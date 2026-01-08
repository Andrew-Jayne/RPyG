import json
import os
from logging import INFO, FileHandler, Formatter, Logger, LogRecord, getLogger
from typing import override


def ensure_type(
    instance: object,
    expected_type: type,
    variable_name: str,
) -> None:
    if isinstance(instance, expected_type) is False:
        raise ValueError(
            f"""
The '{variable_name}' parameter must be of type {expected_type.__name__}.
Received type: {type(instance).__name__}.
"""
        )


class JSONFormatter(Formatter):
    @override
    def format(self, record: LogRecord) -> str:
        log_data = {
            "severity": record.levelname,
            "timestamp": self.formatTime(record, self.datefmt),
            "module": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_data)


def setup_logger(source_module_name: str) -> Logger:
    # Create a handler that writes to a file
    handler = FileHandler("rpyg.jsonl", mode="a")
    handler.setLevel(level=os.environ.get("RPYG_LOG_LEVEL", INFO))

    # Create a formatter
    formatter = JSONFormatter()
    handler.setFormatter(formatter)

    # Configure the root logger
    root_logger = getLogger()
    root_logger.handlers = []  # Remove existing handlers
    root_logger.setLevel(INFO)
    root_logger.addHandler(handler)

    return getLogger(source_module_name)


__all__ = ["ensure_type", "setup_logger"]
