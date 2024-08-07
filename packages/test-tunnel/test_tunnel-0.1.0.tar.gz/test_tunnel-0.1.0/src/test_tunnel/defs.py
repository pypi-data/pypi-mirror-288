# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Common definitions for the tunnel testing library."""

from __future__ import annotations

import dataclasses
import typing


if typing.TYPE_CHECKING:
    import logging
    import pathlib


@dataclasses.dataclass(frozen=True)
class Config:
    """Common configuration for the tunnel testing library.

    This is the base class for the various configuration settings passed to
    the `test-tunnel` library's routines.
    For the present it is used by the functions in the `test_tunnel.addresses` module.
    """

    log: logging.Logger
    """The logger to send diagnostic and informational messages to."""

    offset: int
    """The number of ports to skip when looking for available ones."""

    verbose: bool
    """Has verbose logging been enabled?"""


@dataclasses.dataclass(frozen=True)
class ConfigProg(Config):
    """Common configuration also including a program to test in a UTF-8-capable environment.

    This class extends the base `Config` class, adding the path to the program that will
    be tested (the tunnel proxy/server tool) and a set of variable/value pairs to
    pass to child processes to ensure their output may be parsed as UTF-8 strings.
    """

    prog: pathlib.Path
    """The path to the program to test."""

    utf8_env: dict[str, str]
    """The UTF-8-capable environment settings."""
