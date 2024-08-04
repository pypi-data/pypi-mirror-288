import logging

class DebugLogger:
    _logger = logging.getLogger(__name__)
    debug: bool = False
    
    def log(self, data):
        if self.debug:
            self._logger.debug()
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DebugLogger, cls).__new__(cls)
        return cls.instance
    