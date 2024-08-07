# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Type stubs for the netifaces library."""

from typing import TypedDict


class AddressRecord(TypedDict):
    """A single address record returned for an interface."""

    addr: str
    netmask: str


def interfaces() -> list[str]: ...

def ifaddresses(iface: str) -> dict[int, list[AddressRecord]]: ...
