# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Provide a base class for running tunnel tests.

This module provides the `TestTunnel` class to be used as a base class for implementing
test runners for various tunnel programs.
Its `run()` method sets the test environment up, determines addresses and ports to use for
testing the connections, invokes an implementation-specific method to start the tunnel/proxy
server, and then loops over a predetermined set of connection addresses, again invoking
an implementation-specific method to prepare an established TCP connection for forwarding data.

The `test_tunnel.cmd_test` sample modules may be used as a starting point for implementing
tool-specific test classes using `TestTunnel`.
"""

from __future__ import annotations

import abc
import contextlib
import errno
import sys
import time
import typing

from . import addresses
from . import defs


if typing.TYPE_CHECKING:
    import socket
    import subprocess  # noqa: S404
    from collections.abc import Iterator
    from typing import Final


class TestTunnel(abc.ABC):
    """Base class for running tunnel tests.

    This class mainly provides the `run()` method that determines some addresses and ports to
    use for the connections, sets up a listener, and invokes implementation-specific methods to
    start the tunnel/proxy server and prepare some TCP connections for forwarding data.
    A tool-specific implementation must override at least the `slug()`, `do_spawn_server()`, and
    `do_handshake()` methods.
    """

    cfg: defs.ConfigProg
    """The tunnel proxy configuration."""

    def __init__(self, cfg: defs.ConfigProg) -> None:
        """Store the configuration object."""
        self.cfg = cfg
        self.cfg.log.debug(
            "Using %(locale)s as a UTF-8 locale.",
            {"locale": cfg.utf8_env["LC_ALL"]},
        )

    @abc.abstractmethod
    def slug(self) -> str:
        """Provide a short string to identify the tested tunnel implementation.

        The returned string is used in logging and diagnostic messages so that it is clear
        which tool is being tested.
        """
        raise NotImplementedError

    def do_test_conn_connect(
        self,
        cli_sock: socket.socket,
        address: addresses.Address,
        port: int,
    ) -> None:
        """Connect to the specified address/port.

        This method is invoked internally by `run()` to make sure that the tunnel/proxy
        server started by the `do_spawn_server()` method can at least accept TCP connections at
        the addresses it should have been configured to listen on.
        """
        dest: Final = (address.address, port)
        self.cfg.log.info(
            "Connecting to the %(slug)s server at %(dest)r",
            {"slug": self.slug(), "dest": dest},
        )
        for _ in range(10):
            try:
                cli_sock.connect(dest)
                break
            except OSError as err:
                if err.errno != errno.ECONNREFUSED:
                    raise
                self.cfg.log.debug("Could not connect, waiting for a second")
                time.sleep(1)
        else:
            sys.exit(f"Could not connect to the {self.slug()} server at {dest} after ten attempts")

    def expect_read(
        self,
        sock: socket.socket,
        expected: bytes,
        tag: str,
        *,
        compare_len: int | None = None,
    ) -> bytes:
        """Read some data, make sure it is as expected.

        This method is used internally by `run()` after establishing a TCP connection through
        the tunnel/proxy server (and after the `do_handshake()` method has set the connection up)
        to make sure that the data sent along the connection is forwarded correctly.

        If the `compare_len` parameter is specified, only so many bytes at the start of
        the response are compared; the rest is allowed to vary, although it must still have
        the expected total length in bytes.
        """
        if compare_len is None:
            compare_len = len(expected)

        data: Final = sock.recv(4096)
        self.cfg.log.debug("- got %(data)r", {"data": data})
        if data[:compare_len] != expected[:compare_len]:
            sys.exit(f"Unexpected {tag} (comparing {compare_len} bytes): {expected=!r} {data=!r}")
        return data

    @abc.abstractmethod
    def do_handshake(
        self,
        cli_sock: socket.socket,
        svc_listen: addresses.AddrPort,
    ) -> tuple[addresses.Address, int] | None:
        """Perform the protocol-specific tunnel handshake.

        Once the tunnel/proxy server has been started by `do_spawn_server()` and a client
        connection to it has been established by `run()`, this method sends and receives
        any data necessary for a "handshake" as required by the tunnel protocol, e.g.
        negotiation and authentication for a SOCKS5 proxy, a CONNECT request for
        an HTTP/HTTPS proxy, etc.

        This method may optionally return the source address and port of the forwarded
        connection if it can be obtained from the tunnel protocol, e.g. SOCKS5 will
        sometimes return that information.
        """
        raise NotImplementedError

    def do_test_conn_xfer(
        self,
        cli_sock: socket.socket,
        srv_sock: socket.socket,
        svc_listen: addresses.AddrPort,
    ) -> None:
        """Perform the protocol handshake and conversation.

        Invoked internally by `run()`, this method checks that a client connection to
        the internal server can indeed be established via the tunnel/proxy server
        (using the `do_handshake()` method), and that it can indeed forward data in
        both directions.
        """
        self.do_handshake(cli_sock, svc_listen)

        self.cfg.log.debug("Accepting a connection from the %(slug)s server", {"slug": self.slug()})
        (conn_sock, conn_data) = srv_sock.accept()
        self.cfg.log.debug(
            "- accepted a connection on fd %(fileno)d from %(conn_data)r",
            {"fileno": conn_sock.fileno(), "conn_data": conn_data},
        )
        if conn_sock.family != svc_listen.address.family:
            sys.exit(
                f"Expected a {svc_listen.address.family} family connection, got {conn_sock.family}",
            )

        self.cfg.log.debug("Let's say hello to the client")
        expected: Final = b"Hello"
        conn_sock.send(expected)
        self.cfg.log.debug("Let's try to read that from the client side")
        self.expect_read(cli_sock, expected, "client read")

        self.cfg.log.debug("Closing the client connection")
        cli_sock.close()
        self.cfg.log.debug("Let's get an empty read from the server side")
        self.expect_read(conn_sock, b"", "server side empty read")

        self.cfg.log.debug("Closing the server side of the connection")
        conn_sock.close()

    @abc.abstractmethod
    @contextlib.contextmanager
    def do_spawn_server(
        self,
        proxy_listen: addresses.AddrPort,
        svc_listen: addresses.AddrPort,
    ) -> Iterator[subprocess.Popen[str]]:
        """Spawn the tunnel-specific server process.

        This method will most probably invoke an external program to start
        the implementation-specific tunnel/proxy server.
        It may also possibly create a configuration file in a temporary directory
        before running the program itself.

        It must return a process instance that the `run()` method may monitor and
        wait for after completing the connection and data transfer tests.
        """
        raise NotImplementedError

    def test_conn(
        self,
        proxy_listen: addresses.AddrPort,
        svc_listen: addresses.AddrPort,
    ) -> None:
        """Test the connectivity across a tunnel."""
        self.cfg.log.info(
            "Client at %(proxy_addr)s port %(proxy_port)d",
            {"proxy_addr": proxy_listen.clients[0], "proxy_port": proxy_listen.proxy_port},
        )
        self.cfg.log.info(
            "Proxy at %(listen_addr)s port %(listen_port)d",
            {"listen_addr": proxy_listen.address, "listen_port": proxy_listen.svc_port},
        )
        self.cfg.log.info(
            "Proxy client at %(client_addr)s port %(client_port)d",
            {"client_addr": svc_listen.clients[0], "client_port": svc_listen.proxy_port},
        )
        self.cfg.log.info(
            "Server at %(server_addr)s port %(server_port)d",
            {"server_addr": svc_listen.address, "server_port": svc_listen.svc_port},
        )

        self.cfg.log.info("Creating the server listening socket")
        with addresses.bind_to(self.cfg, svc_listen.address, svc_listen.svc_port) as srv_sock:
            self.cfg.log.debug("Server socket: %(srv_sock)r", {"srv_sock": srv_sock})
            srv_sock.listen(1)

            self.cfg.log.info("Spawning the %(slug)s server process", {"slug": self.slug()})
            with self.do_spawn_server(proxy_listen, svc_listen) as sproc:
                self.cfg.log.debug(
                    "- spawned %(slug)s server at %(pid)d",
                    {"slug": self.slug(), "pid": sproc.pid},
                )

                try:
                    self.cfg.log.info("Creating the client socket")
                    with addresses.bind_to(
                        self.cfg,
                        proxy_listen.clients[0],
                        proxy_listen.proxy_port,
                    ) as cli_sock:
                        self.cfg.log.debug("Client socket: %(cli_sock)r", {"cli_sock": cli_sock})
                        self.do_test_conn_connect(
                            cli_sock,
                            proxy_listen.address,
                            proxy_listen.svc_port,
                        )
                        self.cfg.log.debug("- connected: %(cli_sock)r", {"cli_sock": cli_sock})

                        self.do_test_conn_xfer(cli_sock, srv_sock, svc_listen)

                    self.cfg.log.debug("Stopping the %(slug)s server", {"slug": self.slug()})
                    sproc.terminate()
                    self.cfg.log.debug(
                        "Waiting for the %(slug)s server process to exit",
                        {"slug": self.slug()},
                    )
                    self.cfg.log.info("%(output)r", {"output": sproc.communicate()})
                    self.cfg.log.debug(
                        "%(slug)s server exit code %(res)d",
                        {"slug": self.slug(), "res": sproc.wait()},
                    )
                except BaseException as err:
                    self.cfg.log.debug(
                        "Killing the %(slug)s server because of an exception: %(err)s",
                        {"slug": self.slug(), "err": err},
                    )
                    sproc.kill()
                    raise

    def run(self) -> None:
        """Gather addresses, group them in pairs, run tests.

        This is the main entry point for instances of classes derived from `TestTunnel`.
        It uses the `test_tunnel.addresses` module's routines to determine several
        sets of addresses to use for a client connection, a proxy server, and an internal
        server, and then uses the implementation-specific methods to start a tunnel/proxy
        server, establish a client connection through it, and make sure that data can
        flow both ways.
        """
        self.cfg.log.debug("Starting up")
        apairs: Final = addresses.find_pairs(
            self.cfg,
            addresses.find_ports(self.cfg, addresses.get_addresses(self.cfg)),
        )
        self.cfg.log.info("Connectivity information: address family, server, clients:")
        for family, ports in sorted(apairs.items()):
            self.cfg.log.info("%(family)d", {"family": family})
            for port in ports:
                self.cfg.log.info("\t%(address)s", {"address": port.address.address})
                for client in port.clients:
                    self.cfg.log.info("\t\t%(client)s", {"client": client.address})

        self.cfg.log.info("Picking two pairs for each address family, if possible")
        selected = addresses.pick_pairs(self.cfg, apairs)
        self.cfg.log.info("Testing %(count)d combination(s)", {"count": len(selected)})
        for proxy_listen, svc_listen in selected:
            self.test_conn(proxy_listen, svc_listen)
