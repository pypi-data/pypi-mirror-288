import logging
import tabulate  # type: ignore


class TableFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "Level": record.levelname,
            "Time": self.formatTime(record, self.datefmt),
            "Message": record.getMessage(),
        }
        return tabulate.tabulate([log_entry], headers="keys", tablefmt="grid")


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = TableFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.info(f"An error occurred in {func.__name__}: {e}")
            return None
    return wrapper
