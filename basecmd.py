#!/usr/bin/env python3

"""
Logging boilerplate for the command line.
"""

import logging
import sys
from argparse import ArgumentParser, Namespace
from enum import IntEnum

from colors import color, red, white, yellow
from decouple import config

__all__ = ("BaseCmd",)
__version__ = "0.1.10"


class LogLevel(IntEnum):
    error = logging.ERROR
    warning = logging.WARNING
    info = logging.INFO
    debug = logging.DEBUG

    @classmethod
    def as_dict(cls):
        return {level.name: level.value for level in cls}


class BaseCmd:
    "Provide logging and related command-line arguments"

    DEFAULT_LOG_FORMAT = "%(asctime).19s  %(message)s"
    LOG_FORMAT: str = config("LOG_FORMAT", default=DEFAULT_LOG_FORMAT)

    options: Namespace
    log: logging.Logger

    class ColorFormatter(logging.Formatter):
        "Color log output by log level"

        # See: https://stackoverflow.com/a/56944256

        def __init__(self, format):
            self.default_formatter = logging.Formatter(format)
            self.formats = {
                logging.DEBUG: logging.Formatter(color(format, style="faint")),
                logging.INFO: logging.Formatter(white(format)),
                logging.WARNING: logging.Formatter(yellow(format)),
                logging.ERROR: logging.Formatter(red(format)),
                logging.CRITICAL: logging.Formatter(
                    color(format, fg="red", style="bold")
                ),
            }

        def format(self, record) -> str:
            return self.formats.get(record.levelno, self.default_formatter).format(
                record
            )

    def __init__(self):
        self.parse_args()
        self.init_logging()

    def add_arguments(self) -> None:
        "Hook for subclasses to add additional command line options"

    def parse_args(self, args=None) -> None:
        self.parser = ArgumentParser(description=self.__doc__)

        self.parser.add_argument(
            "-v",
            "--verbosity",
            choices=LogLevel._member_names_,
            default=config("LOG_LEVEL", default="info"),
            help="Logging verbosity",
        )

        self.parser.add_argument(
            "--log-file",
            help="File path for logging",
            default=config("LOG_FILE", default=None),
        )

        self.add_arguments()
        self.options = self.parser.parse_args(args)

    def init_logging(self) -> None:
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(LogLevel.as_dict().get(self.options.verbosity, logging.INFO))

        if self.options.log_file:
            logging.basicConfig(filename=self.options.log_file)
        else:
            logging.basicConfig(stream=sys.stdout)

        self.rootHandler = logging.getLogger().handlers[0]
        self.tty_log = (
            type(self.rootHandler) is logging.StreamHandler
            and self.rootHandler.stream.isatty()  # ty: ignore[unresolved-attribute]
        )
        if self.tty_log:
            self.rootHandler.setFormatter(self.ColorFormatter(self.LOG_FORMAT))
        else:
            self.rootHandler.setFormatter(logging.Formatter(self.LOG_FORMAT))


if __name__ == "__main__":  # Demo code

    class DemoCmd(BaseCmd):
        def __call__(self):
            self.log.debug("Command line options: %s", self.options)

    cmd = DemoCmd()
    cmd()
