import logging


class PicklesLogger:
    name = "pickles_logger"

    def __init__(self, log_level=None):
        self.formatter = logging.Formatter(
            "%(asctime)s [%(levelname)-4.4s] %(message)s"
        )
        self.logger = logging.getLogger()
        self.__init_log_level__(log_level)
        self.__init_console_logger__()

    def __init_log_level__(self, log_level):
        if log_level is None:
            log_level = logging.INFO
        self.logger.setLevel(log_level)

    def __init_console_logger__(self):
        if not [
            h for h in self.logger.handlers if h.__class__ is logging.StreamHandler
        ]:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            self.logger.addHandler(console_handler)

    def log(self, log_type, *args, **kwargs):
        args = list(args)
        args[0] = args[0].ljust(43)
        kwargs_str = " ".join([f"{k}={v}" for k, v in kwargs.items()])
        msg = f"{' '.join(args) + ' ' if args else ''}{kwargs_str}"
        return {
            "info": self.logger.info,
            "warning": self.logger.warning,
            "warn": self.logger.warning,
            "error": self.logger.error,
            "exception": self.logger.exception,
            "critical": self.logger.critical,
            "fatal": self.logger.fatal,
        }[log_type.lower()](msg)
