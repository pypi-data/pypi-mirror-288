from typing import  Callable, 
import asyncio
import socket
import select
import ssl
import time
from queue import Queue, Empty
from enum import Enum
from IrcConnector_Edog0049a.TokenBucket import TokenBucket
from EventHandler_Edog0049a import EventHandler
from IrcConnector_Edog0049a.utils import DebugLogger

debugLog = DebugLogger()

class events(Enum):
    MESSAGE = 1
    CONNECTED = 2
    DISCONNECT = 3
    ERROR = 4 

class IrcConnector():
    """ IRC Conroller

        :param server: address to IRC server
        :type server: str

        :param port: IRC server port
        :type port: int

        :param pingwait: keep alive delay 
        :type ping: int
    """
    EVENTS = events
    def __init__(self, server: str, port: int, SSL:bool=False, pingwait: int=300, Qsize: int=50, maxToken: int=20, tokenRefillTime: int=30)->None:
        # Populate values
        self._server: str = server
        self._port: int = port
        self._SSL:bool = SSL
        self._pingWait: int = pingwait
        self._lastPing: time.time = time.time()
        self._connected: bool = False
        self.isSSL:bool = False
        self._socket: socket.socket | ssl.SSLSocket = self._getNewSocket()
        self._readIO: list = []
        self._writeIO: list = []
        self._errorIO: list  = []
        self._queue: Queue = Queue(Qsize)
        self._tokenBucket = TokenBucket(maxToken=maxToken, timePeriod=tokenRefillTime)
        self._runTask: asyncio.Task
        self._event: EventHandler = EventHandler()
        self.on: Callable = self._event.on
        
    def connect(self)->None:
        """ IrcController.connect - Creates new socket & Opens connection to IRC server  
        
            :return: None
            :rtype: None
        """
        
        self._socket = self._getNewSocket()
        self._readIO.append(self._socket)
        self._writeIO.append(self._socket)
        self._errorIO.append(self._socket)
        try:
            self._socket.connect((self._server, self._port))
            self._connected = True 
        except socket.error as error:
            debugLog.log(error)
            self._event.emit(self, self.EVENTS.ERROR, error)
            self.disconnect()
            
        try:
            asyncio.run(self._run())
        except RuntimeError as error:
            self.task = self._loop.create_task(self._run())

        
    def disconnect(self)->None:
        """
        IrcController.disconnect - Closes sockets & Disconects from IRC server 
        """
        self._readIO = []
        self._writeIO = []
        self._connected = False
        self._socket.close()
    
    def send(self,data):
        data = f"{data}\r\n" if not data.endswith("\r\n") else data
        self._queue.put(data)
    
    def isConnected(self)->bool:
        """ IrcController.isConnected - Gets status of server connection"""
        return self._connected
    
    async def _run(self):
        while self.isConnected:
            await self._receive()
            await self._send()
            await self._errorCheck()


    async def _send(self, data: str=None)->None:
        """ IrcController.send - sends to server 
            
            :param data: string to be sent to IRC server
            :type data: str

            :return: None
            :rtype: None
        """
        try:
            _, writer, _ = select.select(self._readIO, self._writeIO, self._errorIO)
            for sock in writer:
                while self._queue.not_empty and self._tokenBucket.usetoken:
                    data = data if data else self._queue.get_nowait()
                    if data:
                        sock.send(data.encode())
                    await asyncio.sleep(0)
        except socket.error as error:
            debugLog.log(error)
            self._event.emit(self, self.EVENTS.ERROR, error)
            self.disconnect()
        except Empty:
            ...


    async def _receive(self)->None:
        """ IrcController.receive - Receives all data from socket buffer 
        
            :return: All available data from socket buffer, if none is available returns None
            :rtype: str or None
        """
        try:
            await self._ping()
            reader, _, _ = select.select(self._readIO, self._writeIO, self._errorIO)
            for sock in reader:
                buffer = sock.recv(4096)
                try:
                    data: str =  buffer.decode() 
                    if data.startswith("PING"):
                        await self._pong()
                    elif data:
                        self._event.emit(self,self.EVENTS.MESSAGE, data)
                except Exception:
                    ...
        except socket.error as error:
            debugLog.log(error)
            self._event.emit(self, self.EVENTS.ERROR, error)
            self.disconnect()


    async def _ping(self)->None:
        """ IrcController._ping - sends keep alive ping if pingwait timer runs out  
        
            :return: None
            :rtypr: None
        """
        try:
            if time.time() - self._lastPing > self._pingWait:
                self._lastPing = time.time()
                await self._send("PING")
        except socket.error as error:
            self._event.emit(self, self.EVENTS.ERROR, error)
            self.disconnect()
            

    async def _pong(self)->None:
        """ IrcController._pong - replies to server ping 

            :return: None
            :rtypr: None   
        """
        try:
            self._lastPing = time.time()
            await self._send("PONG")
        except socket.error as error:
            self._event.emit(self, self.EVENTS.ERROR, error)
            self.disconnect()
      
    def _getNewSocket(self) -> socket.socket:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self._SSL:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.post_handshake_auth = True
                sock = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=self._server)
                self.isSSL = True
            return sock
    
    async def _errorCheck(self):
        _, _, error = select.select(self._readIO, self._writeIO, self._errorIO)
        for err in error:
            self._event.emit(self, self.EVENTS.ERROR, err)

    @property 
    def _loop(self):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop   

    