"""These are miscellaneous utility functions/classes."""

from __future__ import annotations

import logging
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any

LOGGER = logging.getLogger(__name__)

DECAMELIZE_REGEX = re.compile(r"(?<!^)(?=[A-Z])")

if sys.version_info < (3, 11):
    from backports.datetime_fromisoformat import MonkeyPatch

    MonkeyPatch.patch_fromisoformat()

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


def decamelize(camel_case: str) -> str:
    """Convert CamelCase to snake_case."""
    return DECAMELIZE_REGEX.sub("_", camel_case).lower()


@dataclass
class TailHelper:
    """Tails logs.

    Args:
        print_handler: the way it prints the lines e.g. :py:meth:print
            or a :py:class:logging.Logger
        start_message: the start_message to print before the first line
            or if None it will print a horizontal line
        previous_line_number: the previous line number that was printed, if not none the start_message
            will never be printed and the first line will be the line after :py:attr:previous_line_number
    """

    print_handler: Callable[[str], Any]
    start_message: str | None = None
    previous_line_number: int | None = None

    def tail(self, log_lines: Sequence[str] | None):
        """Handles the logs.

        If :py:attr:TailHelper.previous_line_number is None it will print the :py:attr:TailHelper.start_message
        and print everything contained int :py:attr:logs
        But if the :py:attr:TailHelper.previous_line_number is an integer it will print the
        logs from that given line number, this will only print new lines.

        Args:
            log_lines: a list of lines, if None execution will be skipped
        """
        if log_lines is not None:
            if self.previous_line_number is None:
                if self.start_message:
                    self.print_handler(self.start_message)
                else:
                    print_horizontal_line(print_handler=self.print_handler)
                self.print_handler("\n".join(log_lines))
            else:
                new_lines = log_lines[self.previous_line_number :]
                if new_lines:
                    self.print_handler("\n".join(new_lines))
            self.previous_line_number = len(log_lines)


def print_horizontal_line(c: str = "-", print_handler: Callable[[str], Any] = print):
    """Print a horizontal line with `:py:attr:c`.

    It uses the amount of terminal columns to print a line of good length
    Args:
        c: the char to print
        print_handler: the function to use for printing
    """
    print_handler(c * os.get_terminal_size().columns)


def is_dataset_a_view(dataset_transaction: dict) -> bool:
    """Determines based on a transaction, if a dataset is a view.

    Args:
        dataset_transaction: a transaction on the dataset in question

    Returns:
        bool: if dataset is a view
    """
    return (
        "record" in dataset_transaction
        and "view" in dataset_transaction["record"]
        and dataset_transaction["record"]["view"] is True
    )


def parse_iso(iso_str: str) -> datetime:
    """Parses iso string to datetime."""
    return datetime.fromisoformat(iso_str)
