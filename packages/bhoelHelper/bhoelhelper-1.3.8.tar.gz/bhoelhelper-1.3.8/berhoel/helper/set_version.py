"""Set lib version from `pyproject.toml`.

.. note::

  .. deprecated:: 1.3.6
    Use:

    .. code-block:: python

      __version__ = __import__("importlib.metadata", fromlist=["version"]).version(
          <package name>
      )

    instead

This library allows for setting the version number for a library from
the pyproject.toml file.

Add to your `pyproject.toml` add a new section:

.. code-block:: toml

  [tool.berhoel.helper.set_version]
  version_files = ["berhoel/helper/_version.py"]

Generate the version file:

.. code-block:: shell

  > poetry run set_lib_version
  writing berhoel/helper/_version.py

In the library `__init__.py` just use:

.. code-block:: python

  try:
      from ._version import __version__
  except ImportError:
      __version__ = "0.0.0.invalid0"
"""

import argparse
from importlib import metadata
from pathlib import Path
import sys
import warnings

import tomli

__date__ = "2023/12/26 19:03:33 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020, 2022 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


def build_parser() -> argparse.ArgumentParser:
    """Build cli parser."""
    parser = argparse.ArgumentParser(
        prog="set_lib_version",
        description="Create version files with version number from `pyproject.toml`.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {metadata.version('bhoelHelper')}",
    )
    return parser


def build() -> None:
    """Create version files with version number from `pyproject.toml`."""
    message = "dont use __version__"
    warnings.warn(message, DeprecationWarning, stacklevel=2)

    parser = build_parser()
    parser.parse_args()

    pyproject = (Path() / "pyproject.toml").resolve()

    with pyproject.open("rb") as conf_inp:
        config = tomli.load(conf_inp)

    version = config["tool"]["poetry"]["version"]
    ver_files = config["tool"]["berhoel"]["helper"]["set_version"]["version_files"]
    for ver_file in ver_files:
        sys.stdout.write(f"writing {ver_file!s}\n")
        with Path(ver_file).resolve().open("w") as target:
            target.write(f'__version__ = "{version}"\n')
