import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


class LoggerConfig:
    LOG_DIR = None

    @staticmethod
    def setup_logging_directory(log_directory):
        LoggerConfig.LOG_DIR = log_directory

    @staticmethod
    def get_logger(module_name):
        if LoggerConfig.LOG_DIR is None:
            raise ValueError("Log directory has not been set. Please call setup_logging_directory first.")

        today_str = datetime.now().strftime("%Y-%m-%d")
        log_dir = os.path.join(LoggerConfig.LOG_DIR, today_str)
        os.makedirs(log_dir, exist_ok=True)

        # Use a unique name for each module to prevent logger duplication
        logger = logging.getLogger(module_name)

        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(f'%(asctime)s - {module_name}/%(module)s - %(levelname)s - %(message)s')

            all_handler = TimedRotatingFileHandler(
                filename=os.path.join(log_dir, 'ALL.log'), when='midnight', interval=1, backupCount=30
            )
            all_handler.setLevel(logging.DEBUG)
            all_handler.setFormatter(formatter)
            logger.addHandler(all_handler)

            # Setting up handlers for each log level
            log_levels = {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'ERROR': logging.ERROR,
                'CRITICAL': logging.CRITICAL,
            }

            for level_name, level in log_levels.items():
                handler = TimedRotatingFileHandler(
                    filename=os.path.join(log_dir, f'{level_name.lower()}.log'), when='midnight', interval=1, backupCount=30
                )
                handler.setLevel(level)
                handler.setFormatter(formatter)
                logger.addHandler(handler)

        return logger