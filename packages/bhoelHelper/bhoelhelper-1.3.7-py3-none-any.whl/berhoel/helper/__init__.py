"""Misc helper."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import timedelta
from enum import Enum, auto
import sys
import time
from typing import Callable, Generator

__date__ = "2024/08/03 18:32:45 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 1999, 2000, 2021, 2022 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "bhoel@starship.python.net"


class SwirlSelect(Enum):
    """Selector for swirl style."""

    LINES = auto()
    DOTS = auto()


__swirl_string = {
    SwirlSelect.LINES: r"\|/-",
    SwirlSelect.DOTS: (
        "\N{BRAILLE PATTERN DOTS-123}"  # "⠇"
        "\N{BRAILLE PATTERN DOTS-237}"  # "⡆"
        "\N{BRAILLE PATTERN DOTS-378}"  # "⣄"
        "\N{BRAILLE PATTERN DOTS-678}"  # "⣠"
        "\N{BRAILLE PATTERN DOTS-568}"  # "⢰"
        "\N{BRAILLE PATTERN DOTS-456}"  # "⠸"
        "\N{BRAILLE PATTERN DOTS-145}"  # "⠙"
        "\N{BRAILLE PATTERN DOTS-124}"  # "⠋"
    ),
}


def swirl(style: SwirlSelect = SwirlSelect.LINES) -> Generator:
    r"""Retrun generator to show a swirling life indicator.

    >>> sw = swirl()
    >>> a = [_ for _ in zip(range(5), sw)]
    \...|.../...-...\...
    >>> sw = swirl(SwirlSelect.DOTS)
    >>> a = [_ for _ in zip(range(8), sw)]
    ⠇...⡆...⣄...⣠...⢰...⠸...⠙...⠋...

    Returns:
      `generator`: printing running indicator.
    """
    sw_string = __swirl_string[style]
    while True:
        for c in sw_string:
            sys.stdout.write(f"{c}\r")
            yield


def count_with_msg(msg: str = "loop", start: int = 0) -> Generator:
    """Count variable with start value and message.

    >>> c = count_with_msg("msg", 5)
    >>> print([i for _, i in zip(range(5), c)] == [5, 6, 7, 8, 9])
    msg 1 ...msg 2 ...msg 3 ...msg 4 ...msg 5 ...True
    >>>

    Args:
        msg (str): base message
        start (int): counter start_time

    Returns:
        `generator`: counter with message.
    """
    i = 1
    _count = start
    while True:
        sys.stdout.write(f"{msg} {i} \r")
        yield _count
        _count += 1
        i += 1


@contextmanager
def process_msg_context(msg: str) -> Generator:
    """Provides a context for calling routines and reporting entering and exit.

    >>> with process_msg_context("do something"):
    ...     pass
    do something......do something...done
    >>>

    Args:
        msg (str): message for bracing process.

    Returns:
        `contextmanager`: bracing message.
    """
    sys.stdout.write(f"{msg}...\r")
    yield
    sys.stdout.write(f"{msg}...done\n")


@contextmanager
def timed_process_msg_context(msg: str, time_form: Callable | None = None) -> Generator:
    """Provide a context for calling routines and reporting entering and exit.

    Report spent time.

    >>> with timed_process_msg_context("do something"):
    ...     time.sleep(1)
    do something......do something...done (0:00:01)
    >>> with timed_process_msg_context(
    ...     "do something", lambda t: "{:d}s".format(int(t))
    ... ):
    ...     time.sleep(1)
    do something......do something...done (1s)
    >>>

    Args:
        msg (str): message for bracing process.
        time_form (func): function formatting druntime.

    Returns:
        `contextmanager`: bracing message.
    """
    if time_form is None:

        def time_form(t: float | str) -> timedelta:
            return timedelta(seconds=int(t))

    start_time = time.time()
    sys.stdout.write(f"{msg}...\r")
    yield
    sys.stdout.write(f"{msg}...done ({time_form(time.time() - start_time)})\n")
