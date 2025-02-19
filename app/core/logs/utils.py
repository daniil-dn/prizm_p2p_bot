import logging
import time

from app.core.config import settings
from logging import config


class GMTFormatter(logging.Formatter):
    converter = time.gmtime


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "lines": {
            "format":
                "%(asctime)s [%(levelname)s] %(pathname)s %(lineno)d %(message)s",
            '()':
                GMTFormatter,
        },
        "simple": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            '()': GMTFormatter,
        }
    },
    "handlers": {
        "default": {
            # "level": "DEBUG",
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
        "debug": {
            # "level": "DEBUG",
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "lines"
        }
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False
        },
        "app.bot": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False
        },
        "app.core": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False
        },

    }
}


def config_logging():
    config.dictConfig(LOGGING)