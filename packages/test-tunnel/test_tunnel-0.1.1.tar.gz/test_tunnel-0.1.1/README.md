<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# The test-tunnel library: write tests for network tunnelling utilities

\[[Home][ringlet-home] | [GitLab][gitlab] | [Download][ringlet-download] | [PyPI][pypi] | [ReadTheDocs][readthedocs]\]

## Overview

The `test-tunnel` library's purpose is to make it easy to write either
command-line tools or test modules that start some network tunnelling
server (e.g. stunnel, microsocks, Dante) and verify that it does indeed
forward connections and data as expected.

## A tunnel test scenario

Test classes derived from the `test-tunnel` library's
[TestTunnel][test_tunnel.run_test.TestTunnel] class have
a [run()][test_tunnel.run_test.TestTunnel.run] method that performs
the following actions:

- examines the IPv4 and IPv6 network interfaces currently configured on
  the running system and picks two available ports to listen on for
  each one
- makes a "possible connections" mapping, determining which of these
  addresses may be used as source and destination addresses for TCP
  connections.
  It is possible that some pairs are invalid either due to network protocol
  limitations or due to local system policy.
- picks a set of (server, proxy as client, proxy as server, client)
  address/port combinations from the above mapping so that the client may
  connect to the proxy and the proxy, in turn, may connect to the server

## Writing a test class for a new tool

To write a new test class it is enough to create a new Python class
derived from [test_tunnel.run_test.TestTunnel][] and implement at least
the three methods defined as abstract in that base class:

- [slug()][test_tunnel.run_test.TestTunnel.slug]: return a short text string
  used in log messages to identify the tested program (e.g. "microsocks", "socat")
- [do_spawn_server()][test_tunnel.run_test.TestTunnel.do_spawn_server]:
  start the tested tool with the specified address and port to listen on and
  address and port to forward connections to.
  This method may possibly prepare a configuration file if the tool needs it, or
  it may start the tool and pass the addresses and ports directly on the command line
  if supported.
- [do_handshake()][test_tunnel.run_test.TestTunnel.do_handshake]:
  once a client socket has been connected to the already started tool
  (see the [do_spawn_server()][test_tunnel.run_test.TestTunnel.do_spawn_server] method),
  send and receive any "handshake" data required to make the tool establish
  a connection to the test listener started by the `test-tunnel` library itself.
  For a SOCKS5 server this should be the protocol negotiation and
  authentication, for an HTTP proxy server this would be the `CONNECT`
  request, etc.

## Example tools

The `test-tunnel` library contains two example command-line tools that
implement the test classes for two data forwarding programs:
the [socat][test_tunnel.cmd_test.socat] multipurpose relay tool and
the [microsocks][test_tunnel.cmd_test.microsocks] SOCKS5 server.
They may serve as a starting point for writing new test classes.

## Contact

The `test-tunnel` library was written by [Peter Pentchev][roam].
It is developed in [a GitLab repository][gitlab]. This documentation is
hosted at [Ringlet][ringlet-home] with a copy at [ReadTheDocs][readthedocs].

[roam]: mailto:roam@ringlet.net "Peter Pentchev"
[gitlab]: https://gitlab.com/ppentchev/test-tunnel "The test-tunnel GitLab repository"
[pypi]: https://pypi.org/project/test-tunnel/ "The test-tunnel Python Package Index page"
[readthedocs]: https://test-tunnel.readthedocs.io/ "The test-tunnel ReadTheDocs page"
[ringlet-home]: https://devel.ringlet.net/net/test-tunnel/ "The Ringlet test-tunnel homepage"
[ringlet-download]: https://devel.ringlet.net/net/test-tunnel/download/ "The Ringlet test-tunnel download homepage"
