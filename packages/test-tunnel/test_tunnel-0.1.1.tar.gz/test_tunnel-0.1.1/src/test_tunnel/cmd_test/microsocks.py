# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Run some tests on the microsocks proxy server and client."""

from __future__ import annotations

import contextlib
import dataclasses
import socket
import struct
import subprocess  # noqa: S404
import typing

from test_tunnel import addresses
from test_tunnel import run_test
from test_tunnel.cmd_test import util as cmd_util


if typing.TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Final

    from test_tunnel import defs


ATYP_INET: Final = 1
"""The SOCKS5 address type for IPv4."""

ATYP_INET6: Final = 4
"""The SOCKS5 address type for IPv6."""


@dataclasses.dataclass
class UnsupportedAddressTypeError(Exception):
    """An unsupported address family was specified."""

    atyp: int

    def __str__(self) -> str:
        """Provide a human-readable description of the error."""
        return f"Unsupported SOCKS5 address type {self.atyp}"


class TestMicroSOCKS(run_test.TestTunnel):
    """Run the tunnel tests using a microsocks server."""

    def slug(self) -> str:
        """Identify the microsocks tunnel."""
        return "microsocks"

    @classmethod
    def quirk_server_returns_null_ipv4_response(cls) -> bool:
        """Expect 4 + 2 zeroes as a response to the "connect" request.

        The microsocks server does not bother returning any connection information in
        the response to the "connect" request; instead, it returns an address type of
        IPv4 and four + two bytes of zeroes.
        """
        return True

    def do_handshake(
        self,
        cli_sock: socket.socket,
        svc_listen: addresses.AddrPort,
    ) -> tuple[addresses.Address, int] | None:
        """Perform the SOCKS5 handshake."""

        def get_atyp(family: int) -> int:
            """Get the SOCKS5 "address type" value depending on the address family."""
            if family == socket.AF_INET:
                return ATYP_INET
            if family == socket.AF_INET6:
                return ATYP_INET6
            raise addresses.UnsupportedAddressFamilyError(family)

        def get_family(atyp: int) -> int:
            """Get the IP address family depending on the SOCKS5 "address type" value."""
            if atyp == ATYP_INET:
                return socket.AF_INET
            if atyp == ATYP_INET6:
                return socket.AF_INET6
            raise UnsupportedAddressTypeError(atyp)

        self.cfg.log.debug("Sending 'none' auth")
        cli_sock.send(bytes([5, 1, 0]))

        self.cfg.log.debug("Waiting for the server's auth response")
        self.expect_read(cli_sock, bytes([5, 0]), "auth response")

        family: Final = get_atyp(svc_listen.address.family)
        data: Final = (
            bytes([5, 1, 0, family])
            + svc_listen.address.packed
            + struct.pack(">h", svc_listen.svc_port)
        )
        self.cfg.log.debug("Sending a SOCKS5 CONNECT request: %(data)r", {"data": data})
        cli_sock.send(data)

        self.cfg.log.debug("Waiting for the server's connect response")
        ack = bytes([5, 0, 0])
        if self.quirk_server_returns_null_ipv4_response():
            ack += bytes([1] + [0] * 4 + [0] * 2)
            self.expect_read(cli_sock, ack, "connect response")
            return None

        ack += bytes([family])
        compare_len: Final = len(ack)
        ack += bytes([0] * len(svc_listen.address.packed) + [0] * 2)
        resp: Final = self.expect_read(cli_sock, ack, "connect response", compare_len=compare_len)
        res_family, buf_addr, buf_port = (
            get_family(resp[compare_len - 1]),
            resp[compare_len:-2],
            resp[-2:],
        )
        res_addr: Final = addresses.ipclass(res_family)(buf_addr)
        res_port: Final = struct.unpack(">h", buf_port)[0]
        return (
            addresses.Address(family=res_family, address=str(res_addr), packed=buf_addr),
            res_port,
        )

    @contextlib.contextmanager
    def do_spawn_server(
        self,
        proxy_listen: addresses.AddrPort,
        svc_listen: addresses.AddrPort,
    ) -> Iterator[subprocess.Popen[str]]:
        """Spawn the microsocks proxy process."""
        yield subprocess.Popen(  # noqa: S603
            [
                self.cfg.prog,
                "-i",
                proxy_listen.address.address,
                "-p",
                str(proxy_listen.svc_port),
                "-b",
                svc_listen.clients[0].address,
            ],
            bufsize=0,
            encoding="UTF-8",
            env=self.cfg.utf8_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )


@cmd_util.click_common_args("microsocks")
def main(cfg: defs.ConfigProg) -> None:
    """Parse command-line arguments, prepare the environment, run tests."""
    tester: Final = TestMicroSOCKS(cfg)
    tester.run()


if __name__ == "__main__":
    main()
