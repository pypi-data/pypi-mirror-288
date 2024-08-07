# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Common utilities for the command-line test tools."""

from __future__ import annotations

import logging
import pathlib
import sys
import typing

import click
import utf8_locale

from test_tunnel import defs


if typing.TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Final


def build_logger(*, verbose: bool) -> logging.Logger:
    """Build the logger to send diagnostic and informational messages to."""
    logger: Final = logging.getLogger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    diag_handler: Final = logging.StreamHandler(sys.stderr)
    diag_handler.setLevel(logging.DEBUG)
    diag_handler.addFilter(lambda rec: rec.levelno == logging.DEBUG)
    logger.addHandler(diag_handler)

    info_handler: Final = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(logging.INFO)
    info_handler.addFilter(lambda rec: rec.levelno == logging.INFO)
    logger.addHandler(info_handler)

    err_handler: Final = logging.StreamHandler(sys.stderr)
    err_handler.setLevel(logging.WARNING)
    logger.addHandler(err_handler)

    return logger


def click_common_args(
    prog: str,
) -> Callable[[Callable[[defs.ConfigProg], None]], Callable[[], None]]:
    """Wrap a main function, process the common options."""

    def wrap_wrapper(func: Callable[[defs.ConfigProg], None]) -> Callable[[], None]:
        """Wrap the main function, process the common options."""

        @click.command(name=prog, help=f"Run the {prog} test.")
        @click.option(
            "-O",
            "--offset",
            type=int,
            default=0,
            help="the number of ports to skip when looking for available ones",
        )
        @click.option(
            "-p",
            "--prog",
            type=pathlib.Path,
            required=True,
            help="the path to the program to test",
        )
        @click.option(
            "-v",
            "--verbose",
            is_flag=True,
            help="verbose mode; display diagnostic output",
        )
        def wrapper(*, offset: int, prog: pathlib.Path, verbose: bool) -> None:
            """Run the tunnel test."""
            cfg = defs.ConfigProg(
                log=build_logger(verbose=verbose),
                offset=offset,
                verbose=verbose,
                prog=prog,
                utf8_env=utf8_locale.get_utf8_env(),
            )
            func(cfg)

        return wrapper

    return wrap_wrapper
