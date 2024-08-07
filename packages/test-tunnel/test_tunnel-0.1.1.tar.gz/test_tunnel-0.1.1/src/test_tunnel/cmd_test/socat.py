# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Run some tests using the socat tool in forwarding mode."""

from __future__ import annotations

import contextlib
import subprocess  # noqa: S404
import typing

from test_tunnel import addresses
from test_tunnel import run_test
from test_tunnel.cmd_test import util as cmd_util


if typing.TYPE_CHECKING:
    import socket
    from collections.abc import Iterator
    from typing import Final

    from test_tunnel import defs


class TestSoCat(run_test.TestTunnel):
    """Run the tunnel tests using a socat instance."""

    def slug(self) -> str:
        """Identify the socat tool."""
        return "socat"

    def do_handshake(
        self,
        cli_sock: socket.socket,
        svc_listen: addresses.AddrPort,
    ) -> tuple[addresses.Address, int] | None:
        """No handshake for socat."""
        self.cfg.log.info("No handshake necessary for socat")
        self.cfg.log.debug(
            "Nothing to do for a %(cli)s / %(svc)s connection",
            {"cli": cli_sock, "svc": svc_listen},
        )
        return None

    @contextlib.contextmanager
    def do_spawn_server(
        self,
        proxy_listen: addresses.AddrPort,
        svc_listen: addresses.AddrPort,
    ) -> Iterator[subprocess.Popen[str]]:
        """Spawn the socat proxy process."""
        yield subprocess.Popen(  # noqa: S603
            [
                self.cfg.prog,
                "-v",
                (
                    f"TCP{addresses.family_id(proxy_listen.address.family)}-LISTEN:"
                    f"{proxy_listen.svc_port},"
                    f"bind=[{proxy_listen.address.address}],reuseaddr,fork"
                ),
                (
                    f"TCP{addresses.family_id(svc_listen.clients[0].family)}:"
                    f"[{svc_listen.address.address}]:{svc_listen.svc_port},"
                    f"bind=[{svc_listen.clients[0].address}]"
                ),
            ],
            bufsize=0,
            encoding="UTF-8",
            env=self.cfg.utf8_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )


@cmd_util.click_common_args("socat")
def main(cfg: defs.ConfigProg) -> None:
    """Parse command-line arguments, prepare the environment, run tests."""
    tester: Final = TestSoCat(cfg)
    tester.run()


if __name__ == "__main__":
    main()
