# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Find addresses and ports for the tunnel testing library.

This module contains helper functions for obtaining the IPv4 and IPv6 addresses of
the system's network interfaces, determining which port numbers are available for
listening on each of those addresses, and then determining which pairs of addresses may be
used as source and destination for TCP connections.
Its purpose is to enable a testing tool to listen on one address and establish
a client connection from another one, with the listener and the client possibly in
separate processes (or even programs).
"""

from __future__ import annotations

import dataclasses
import ipaddress
import itertools
import random
import socket
import sys
import typing

import netifaces


if typing.TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Final

    from . import defs


@dataclasses.dataclass
class UnsupportedAddressFamilyError(Exception):
    """An unsupported address family was specified."""

    family: int

    def __str__(self) -> str:
        """Provide a human-readable description of the error."""
        return f"Unsupported address family {self.family}"


@dataclasses.dataclass(frozen=True, order=True)
class Address:
    """Information about a single network address on the system."""

    family: int
    address: str
    packed: bytes


@dataclasses.dataclass(frozen=True)
class AddrPort:
    """An address and two "free" ports to listen on during the test run."""

    address: Address
    svc_port: int
    proxy_port: int
    clients: list[Address]


IPClassType = type[ipaddress.IPv4Address] | type[ipaddress.IPv6Address]


@dataclasses.dataclass(frozen=True)
class _IPFamily:
    """An IP address family and the corresponding ipaddress class."""

    family: int
    short_id: str
    ipcls: IPClassType
    max_prefix_length: int


_FAMILIES: list[_IPFamily] = [
    _IPFamily(socket.AF_INET, "4", ipaddress.IPv4Address, 32),
    _IPFamily(socket.AF_INET6, "6", ipaddress.IPv6Address, 128),
]


def get_addresses(cfg: defs.Config) -> list[Address]:
    """Get the IPv4 and IPv6 addresses on this system."""
    cfg.log.debug("Enumerating the system network interfaces")
    ifaces: Final = netifaces.interfaces()
    cfg.log.debug("- got %(count)d interface names", {"count": len(ifaces)})
    if not ifaces:
        return []

    def add_addresses(
        family: int,
        ipcls: IPClassType,
        addrs: Iterable[str],
    ) -> list[Address]:
        """Create objects for the IPv4/IPv6 addresses found on an interface."""
        res: Final = []
        for addr in addrs:
            try:
                ipaddr = ipcls(addr)
            except ValueError as err:
                cfg.log.debug(
                    "- could not parse the %(addr)r address: %(err)s",
                    {"addr": addr, "err": err},
                )
                continue

            res.append(Address(family=family, address=addr, packed=ipaddr.packed))
            cfg.log.debug("- added %(addr)r", {"addr": res[-1]})

        return res

    return sorted(
        itertools.chain(
            *(
                add_addresses(
                    ipfamily.family,
                    ipfamily.ipcls,
                    (addr["addr"] for addr in addrs.get(ipfamily.family, [])),
                )
                for addrs, ipfamily in itertools.product(
                    (netifaces.ifaddresses(iface) for iface in netifaces.interfaces()),
                    _FAMILIES,
                )
            ),
        ),
    )


def bind_to(cfg: defs.Config, addr: Address, port: int) -> socket.socket:
    """Bind to the specified port on the specified address."""
    try:
        sock: Final = socket.socket(addr.family, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    except OSError as err:
        cfg.log.debug(
            "Could not create a family %(family)d socket: %(err)s",
            {"family": addr.family, "err": err},
        )
        raise

    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except OSError as err:
        cfg.log.debug("Could not set the reuse-port option: %(err)s", {"err": err})
        sock.close()
        raise

    try:
        sock.bind((addr.address, port))
    except OSError as err:
        cfg.log.debug(
            "Could not bind to port %(port)d on %(addr)s: %(err)s",
            {"port": port, "addr": addr.address, "err": err},
        )
        sock.close()
        raise

    return sock


def _find_available_port(cfg: defs.Config, addr: Address, port: int) -> int | None:
    """Find a port to listen on at the specified address."""
    try:
        sock = bind_to(cfg, addr, 0)
    except OSError:
        return None

    cfg.log.debug("  - bound to a random port: %(sockname)r", {"sockname": sock.getsockname()})
    sock.close()

    for _ in range(100):
        port += random.randint(10, 30)  # noqa: S311
        cfg.log.debug("- trying %(port)d", {"port": port})
        try:
            sock = bind_to(cfg, addr, port)
        except OSError:
            continue

        cfg.log.debug("  - success!")
        sock.close()
        return port

    cfg.log.debug("- could not find an available port at all...")
    return None


def find_ports(cfg: defs.Config, addrs: list[Address], first_port: int = 6374) -> list[AddrPort]:
    """Find two ports per network address to listen on.

    The search starts from `first_port + cfg.offset` as a port number.
    Port numbers are never reused, even for different addresses.
    """
    res: Final[list[AddrPort]] = []
    first_port += cfg.offset
    for addr in addrs:
        cfg.log.debug(
            "Looking for a service port to listen on for %(addr)s family %(family)d",
            {"addr": addr.address, "family": addr.family},
        )
        svc_port = _find_available_port(cfg, addr, first_port)
        if svc_port is None:
            cfg.log.debug("Could not find a service port on %(addr)s", {"addr": addr.address})
            continue

        cfg.log.debug("Looking for a proxy port to listen on for %(addr)s", {"addr": addr.address})
        proxy_port = _find_available_port(cfg, addr, svc_port)
        if proxy_port is None:
            cfg.log.debug("Could not find a service port on %(addr)s", {"addr": addr.address})
            continue

        res.append(
            AddrPort(
                address=addr,
                svc_port=svc_port,
                proxy_port=proxy_port,
                clients=[],
            ),
        )
        cfg.log.debug("Added %(addr)r", {"addr": res[-1]})

        # Make sure we never pick the same port, even on different addresses, just in case
        first_port = proxy_port

    return res


def _check_connect(cfg: defs.Config, server: socket.socket, client: Address) -> bool:
    """Check whether a client socket can connect to the server one."""
    cfg.log.debug(
        "- checking whether %(client)s can connect to %(server)r",
        {"client": client.address, "server": server},
    )
    with bind_to(cfg, client, 0) as sock:
        cfg.log.debug("  - got client socket %(sock)r", {"sock": sock})
        try:
            sock.connect(server.getsockname())
        except OSError as err:
            cfg.log.debug("  - failed to connect: %(err)s", {"err": err})
            return False

        try:
            csock, cdata = server.accept()
        except OSError as err:
            cfg.log.debug("  - failed to accept the connection: %(err)s", {"err": err})
            return False

        cfg.log.debug("  - got socket %(csock)r data %(cdata)r", {"csock": csock, "cdata": cdata})

        try:
            if (
                csock.getsockname() != sock.getpeername()
                or csock.getpeername() != sock.getsockname()
            ):
                cfg.log.debug(
                    "  - get*name() mismatch between %(csock)r and %(sock)r",
                    {"csock": csock, "sock": sock},
                )
                return False

            cfg.log.debug("  - success!")
            return True
        finally:
            csock.close()


def find_pairs(cfg: defs.Config, ports: list[AddrPort]) -> dict[int, list[AddrPort]]:
    """Figure out which addresses can connect to which other addresses."""

    def find_single(port: AddrPort, others: Iterable[AddrPort]) -> AddrPort:
        """Find which clients can connect to the specified server port."""
        cfg.log.debug("Checking whether we can connect to %(addr)s", {"addr": port.address.address})
        with bind_to(cfg, port.address, port.svc_port) as svc_sock:
            svc_sock.listen(10)
            with bind_to(cfg, port.address, port.proxy_port) as proxy_sock:
                proxy_sock.listen(10)
                return dataclasses.replace(
                    port,
                    clients=[
                        other.address
                        for other in others
                        if _check_connect(cfg, svc_sock, other.address)
                        and _check_connect(cfg, proxy_sock, other.address)
                    ],
                )

    return {
        family: data
        for family, data in (
            (
                family,
                [
                    res_port
                    for res_port in (
                        find_single(port, (other for other in lports if other != port))
                        for port in lports
                    )
                    if res_port.clients
                ],
            )
            for family, lports in (
                (family, list(fports))
                for family, fports in itertools.groupby(ports, lambda port: port.address.family)
            )
        )
        if data
    }


def pick_pairs(
    cfg: defs.Config,
    apairs: dict[int, list[AddrPort]],
) -> list[tuple[AddrPort, AddrPort]]:
    """Pick two (maybe the same) addresses for each family."""

    def reorder(server: Address, clients: list[Address]) -> list[Address]:
        """Sort the addresses, put the server's own address at the end."""
        return [addr for addr in sorted(clients) if addr != server] + [
            addr for addr in clients if addr == server
        ]

    res: Final[dict[int, tuple[AddrPort, AddrPort]]] = {}
    for family, pairs in apairs.items():
        if len(pairs) == 1:
            cfg.log.debug("Considering a single set for %(family)r", {"family": family})
            first = pairs[0]
            clients = reorder(first.address, first.clients)
            r_first = dataclasses.replace(first, clients=[clients[0]])
            r_second = dataclasses.replace(
                first,
                clients=[clients[0] if len(clients) == 1 else clients[1]],
            )
        else:
            cfg.log.debug("Considering two sets for %(family)r", {"family": family})
            first, second = pairs[0], pairs[1]
            c_first, c_second = (
                reorder(first.address, first.clients),
                reorder(second.address, second.clients),
            )
            r_first, r_second = (
                dataclasses.replace(first, clients=[c_first[0]]),
                dataclasses.replace(second, clients=[c_second[0]]),
            )

        if len(r_first.clients) != 1 or len(r_second.clients) != 1:
            sys.exit(
                f"Internal error: unexpected number of clients: "
                f"{r_first.clients=!r} {r_second.clients=!r}",
            )
        if (r_first.address, {r_first.svc_port, r_first.proxy_port}) == (
            r_second.address,
            {r_second.svc_port, r_second.proxy_port},
        ):
            # So basically we only have a single address to work with...
            cfg.log.debug(
                "Looking for more ports to listen on at %(second)s",
                {"second": r_second.address},
            )
            more_ports = find_ports(
                cfg,
                [r_second.address],
                first_port=max(r_second.svc_port, r_second.proxy_port) + 1,
            )[0]
            r_second = dataclasses.replace(
                r_second,
                svc_port=more_ports.svc_port,
                proxy_port=more_ports.proxy_port,
            )
            if {r_first.svc_port, r_first.proxy_port} == {
                r_second.svc_port,
                r_second.proxy_port,
            }:
                sys.exit(
                    f"Internal error: duplicate port pairs: "
                    f"{r_first.svc_port!r} {r_first.proxy_port!r} "
                    f"{r_second.svc_port!r} {r_second.proxy_port!r}",
                )

        res[family] = (r_first, r_second)
        cfg.log.debug(
            "Address family %(family)r: picked %(addr)r",
            {"family": family, "addr": res[family]},
        )

    return [
        (res[first][0], res[second][1])
        for first, second in itertools.product(res.keys(), res.keys())
    ]


def family_id(family: int) -> str:
    """Return a '4' or '6' specification depending on the address family."""
    try:
        return next(ipfamily.short_id for ipfamily in _FAMILIES if ipfamily.family == family)
    except StopIteration as err:
        raise UnsupportedAddressFamilyError(family=family) from err


def prefix_length(family: int) -> int:
    """Return the maximum prefix length - 32 or 128 - depending on the address family."""
    try:
        return next(
            ipfamily.max_prefix_length for ipfamily in _FAMILIES if ipfamily.family == family
        )
    except StopIteration as err:
        raise UnsupportedAddressFamilyError(family=family) from err


def ipclass(family: int) -> IPClassType:
    """Return the IP address class appropriate for the address family."""
    try:
        return next(ipfamily.ipcls for ipfamily in _FAMILIES if ipfamily.family == family)
    except StopIteration as err:
        raise UnsupportedAddressFamilyError(family=family) from err
