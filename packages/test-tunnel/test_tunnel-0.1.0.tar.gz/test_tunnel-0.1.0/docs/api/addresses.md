<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# The test-tunnel network address discovery module

::: test_tunnel.addresses
    options:
      members: []

## Data structures

::: test_tunnel.addresses.Address
::: test_tunnel.addresses.AddrPort

## Exceptions

::: test_tunnel.addresses.UnsupportedAddressFamilyError

## Address and port discovery routines

::: test_tunnel.addresses.get_addresses

::: test_tunnel.addresses.find_ports

## Address selection and combining routines

::: test_tunnel.addresses.find_pairs

::: test_tunnel.addresses.pick_pairs

## Utility functions

::: test_tunnel.addresses.family_id

::: test_tunnel.addresses.bind_to
