import datetime
import logging
import logging.handlers
import os
from typing import Optional, Literal
import inspect

class IFTLogger:
    """IFT Logging functionality."""

    def __init__(
            self, 
            app_name : str,
            service_name : str,
            log_level: Optional[Literal['debug', 'warning', 'info', 'critical']] = 'debug',
            log_path : str = None,
            write_file : bool = False
        ) -> None:
        """
        Constructor method.

        :param app_name: name of the application i.e. MyApp etc ...
        :type app_name: str
        :param service_name: service name like input_file_generator, pathways, itr etc ...
        :type service_name: str        
        :param log_path: path where the log file will be written to, defaults to None
        :type log_path: str, optional
        :param write_file: if the log messages should be sink to a file, defaults to False
        :type write_file: bool, optional
        :Examples:
            >>> from ift_global import IFTLogger
            >>> my_logger = IFTLogger(
            ...     app_name = 'trade_ingestion',
            ...     service_name = 'data_input'
            ...     )
            >>> my_logger.logger.warning('This is a warning message')
            >>> my_logger.logger.error('This is an error message')
            >>> my_logger.logger.info('This is an info message')
            >>> my_logger.logger = 'ift_common.this_module.this_file.py'
        """
        self.app_name = app_name
        self.service_name = service_name
        self.write_file = write_file
        self.log_level = log_level
        self.log_path = log_path
        self._logger = self._init_logger()

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = self._init_logger(value=value)
        self._remove_old_handlers()
    
    def _get_log_level(self):       
        log_levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        return log_levels.get(self.log_level, logging.DEBUG)
    
    def _init_logger(self, value = None):
        self._logger_id()

        logging.basicConfig(
            level=self._get_log_level(),
        )
        if value:
            logger = logging.getLogger(value)
        else:
            logger = logging.getLogger(__name__)
        console_handler = self._config_console_handler()
        logger.addHandler(console_handler)

        if self.write_file:
            file_handler = self._config_logfile_handler()
            logger.addHandler(file_handler)
        logger.propagate = False
        return logger

    def _log_file_name(self):
        """Builds file path to log file.

        :return: file path to log file
        :rtype: str
        """
        log_file = self.app_name + '.log'
        if not self.log_path:
            return './' + log_file
        else:
            return os.path.join(self.log_path, log_file)

    def _config_logfile_handler(self) -> logging.handlers:
        """Config write log file.

        :return: handlers to write to .log file
        :rtype: logging.handlers
        """
        fh = logging.handlers.RotatingFileHandler(
            self._log_file_name(), mode='a', maxBytes=2000, backupCount=10
        )
        formatter = logging.Formatter(
            fmt=f'%(asctime)s | {self.app_name} | {self.service_name} | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        fh.setFormatter(formatter)
        fh.setLevel(self._get_log_level())
        fh.set_name(f'{self._logger_uid}_writer')
        return fh

    def _config_console_handler(self) -> logging.handlers:
        """Config console handler.

        :return: returns stream handler for print to console log
        :rtype: logging.StreamHandler
        """
        ch = logging.StreamHandler()
        ch.setLevel(self._get_log_level())
        formatter = logging.Formatter(
            fmt=f'%(asctime)s | {self.app_name} | {self.service_name} | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        ch.set_name(f'{self._logger_uid}_console')
        return ch

    def _logger_id(self):
        time_log = datetime.datetime.now()
        time_tostr = datetime.datetime.strftime(time_log, '%y%m%d%H%M%S')
        self._logger_uid = '_'.join(
            (
                self.app_name.lower(),
                self.service_name.lower(),
                time_tostr,
            )
        )
    def _remove_old_handlers(self):

        log_remove = [
            han
            for han in self._logger.handlers
            if not han.name.startswith(self._logger_uid)
        ]
        if not log_remove:
            return True

        for lg in log_remove:

            self._logger.removeHandler(lg)

    def _standard_logging_line(self):

        return f'%(asctime)s | {self.app_name} | {self.service_name} | %(levelname)-8s | %(message)s'

    def _standard_logging_message(self):

        return f'%(asctime)s | {self.app_name} | {self.service_name} | %(levelname)-8s | %(message)s'
    
    def _get_caller_info(self):
        # Get the caller's frame
        try:            
            frame = inspect.stack()[2]            
            filename = os.path.basename(frame.filename)
            return filename, frame.lineno
        except IndexError:
            print('Index Error inspect stack out of range')
            return 'unknown_file', 'unknow_line'
        
    def debug(self, message):
        """Log a debug message."""
        filename, lineno = self._get_caller_info()
        self.logger.debug(f"{filename} | line: {lineno} | {message}")

    def info(self, message):
        """Log an info message."""
        filename, lineno = self._get_caller_info()
        self.logger.info(f"{filename} | line: {lineno} | {message}")

    def warning(self, message):
        """Log a warning message."""
        filename, lineno = self._get_caller_info()
        self.logger.warning(f"{filename} | line: {lineno} | {message}")

    def error(self, message):
        """Log an error message."""
        filename, lineno = self._get_caller_info()
        self.logger.error(f"{filename} | line: {lineno} | {message}")

    def critical(self, message):
        """Log a critical message."""
        filename, lineno = self._get_caller_info()
        self.logger.critical(f"{filename} | line: {lineno} | {message}")