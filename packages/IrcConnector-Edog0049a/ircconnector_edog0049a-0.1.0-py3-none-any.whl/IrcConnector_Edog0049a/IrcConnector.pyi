from IrcConnector_Edog0049a.TokenBucket import TokenBucket as TokenBucket
from IrcConnector_Edog0049a.utils import DebugLogger as DebugLogger
from _typeshed import Incomplete
from enum import Enum

debugLog: Incomplete

class events(Enum):
    MESSAGE = 1
    CONNECTED = 2
    DISCONNECT = 3
    ERROR = 4

class IrcConnector:
    EVENTS = events
    isSSL: bool
    on: Incomplete
    def __init__(self, server: str, port: int, SSL: bool = False, pingwait: int = 300, Qsize: int = 50, maxToken: int = 20, tokenRefillTime: int = 30) -> None: ...
    task: Incomplete
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    def send(self, data) -> None: ...
    def isConnected(self) -> bool: ...
