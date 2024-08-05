"""Proccess arguments flexible.

This module provides a class named ``CheckArgs`` and a function named
``check_args``.

The class ``CheckArgs`` is ment to be used as base class for own
classes.  After the ``__init__`` method is called a dictionary args is
added to the local namespace.

The init mathod has four arguments.

The first is, as usual, the ``self`` handler.  The second is a list or
tuples holding the allowed keyword arguments as first tuple element
and their default values as remaining tuple elements.

The third and forth argument are the ``*data`` and ``**kw`` arguments
from the implemented class.

Example:
  >>> from .check_args import CheckArgs
  >>> class samp(CheckArgs):
  ...     default = (("A", "A"), ("B", "B"), ("C", ("C", 1, 2)))
  ...
  ...     def __init__(self, *data, **kw):
  ...         CheckArgs.__init__(self, *data, **kw)
  ...         print(self.args["A"], self.args["B"], self.args["C"])
  >>> A = samp(A=34)
  34 B ('C', 1, 2)
  >>> A = samp(34, "HALLO")
  34 HALLO ('C', 1, 2)
  >>>

The function ``check_args`` provides similar funtionality for
functions.  It also takes four arguments.

The first to third argument are simlar to the second to forth element
of the class.  The forth element of the function is the functions
name.

Example:
  >>> from .check_args import check_args
  >>> def tst(*data, **kw):
  ...     default = (("A", "A"), ("B", "B"), ("C", ("C", 1, 2)))
  ...     return check_args(default, data, kw, "tst")
  >>> tst(A=34) == {"A": 34, "B": "B", "C": ("C", 1, 2)}
  True
  >>> tst(34) == {"A": 34, "B": "B", "C": ("C", 1, 2)}
  True
  >>>
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

__date__ = "2024/08/03 20:57:55 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 1998-2000,2018 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


class ArgError(TypeError):
    """Error from the argument checking."""


class CheckArgs(ABC):
    """A wrapper around the ``check_args`` function.

    Args:
        default (tuple[tuple[str, object]]): argument names and default values for
              ``__init__`` method.
        data (tuple): arguments to ``__init__`` method.
        kw (dict): keyword arguments to ``__init__`` method.

    Returns:
    dict: argument name, value pairs.
    """

    def __init__(self, *data: tuple, **kw: dict) -> None:
        """Intialize instance."""
        self.args = check_args(self.default, data, kw, self.__class__.__name__)

    @property
    @abstractmethod
    def default(self) -> Iterable[tuple[str, object]]:
        """Return default values."""
        return ()


def check_args(
    default: Iterable[tuple[str, object]], data: tuple, kw: dict, name: str
) -> dict[str, object]:
    """Check arguments for function.

    Args:
        default (tuple[tuple[str, object]]): argument names and default values for
              function call.
        data (tuple): arguments to function call.
        kw (dict): keyword arguments to function call.
        name (str): name for reporting.

    Returns:
    dict: argument name, value pairs.
    """
    args = dict(default)
    arglen = len(args)
    if (len(data) + len(kw)) > arglen:
        msg = f"{name} requires at most {arglen} argument; {len(data)} given"
        raise ArgError
    arglist = []
    for default_, data_ in zip(default, data):
        args[default_[0]] = data_
        arglist.append(default_[0])
    for k in arglist:
        if k in kw:
            msg = f"{name}: key '{k}' used in **kw argument is also set by *data."
            raise ArgError(msg)
    args.update(kw)
    if len(args) != arglen:
        out = list(args.keys())
        for key, _ in default:
            out.remove(key)
        msg = f"{name}: unexpected keyword argument: {out[0]}"
        raise ArgError(msg)
    return args
