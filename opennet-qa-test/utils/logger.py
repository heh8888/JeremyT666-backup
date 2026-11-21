import logging
from pathlib import Path
from datetime import datetime
from config.config import BASE_DIR


class Logger:
    
    def __init__(self, name="opennet", log_dir=None):
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 清除所有現有的 handler
        self.logger.handlers.clear()
        
        if log_dir is None:
            log_dir = BASE_DIR / "logs"
        else:
            log_dir = Path(log_dir)
        log_dir.mkdir(exist_ok=True)
        
        # 日誌檔案名稱

        log_filename = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_file = log_dir / log_filename
        
        file_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_formatter = logging.Formatter(
            '%(message)s'  # 終端機只顯示訊息，保持簡潔
        )
        
        # 1. 檔案處理器（記錄所有 DEBUG 以上的訊息）
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        
        self.log_file = log_file
        self._initialized = True
    
    def debug(self, message):
        self.logger.debug(message, stacklevel=2)
    
    def info(self, message):
        self.logger.info(message, stacklevel=2)
    
    def warning(self, message):
        self.logger.warning(message, stacklevel=2)
    
    def error(self, message):
        self.logger.error(message, stacklevel=2)
    
    def critical(self, message):
        self.logger.critical(message, stacklevel=2)
    
    def get_log_file(self):
        return str(self.log_file)


logger = Logger()

def log_info(message):
    logger.logger.info(message, stacklevel=2)


def log_debug(message):
    logger.logger.debug(message, stacklevel=2)


def log_warning(message):
    logger.logger.warning(message, stacklevel=2)


def log_error(message):
    logger.logger.error(message, stacklevel=2)
