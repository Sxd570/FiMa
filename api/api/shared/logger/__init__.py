import logging
from typing import Optional

class Logger:
    def __init__(self, name: Optional[str] = None, level: int = logging.INFO):
        self.logger = logging.getLogger(name if name else __name__)
        self.logger.setLevel(level)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)


    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)


    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)


    def warning(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)


    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
