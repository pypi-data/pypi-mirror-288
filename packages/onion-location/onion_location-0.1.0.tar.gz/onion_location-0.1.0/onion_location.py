#!/usr/bin/python3
# SPDX-FileCopyrightText: © 2024 Frederik “Freso” S. Olesen
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Onion-Location -- discover .onion locations
# Copyright © 2024 Frederik “Freso” S. Olesen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Onion-Location discovery.

This module provides an easy and simple way to discover advertised
`Onion-Location` headers from a given webpage.

.. seealso::

   `Tor Project, Onion-Location <https://community.torproject.org/onion-services/advanced/onion-location/>`_
      Tor Project’s own page about the Onion-Location header.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from urllib.request import urlopen

from bs4 import BeautifulSoup, Tag


def tag_is_onion_location(tag: Tag) -> bool:
    """Check whether a BeautifulSoup Tag is a http-equiv Onion-Location <meta> tag.

    :param tag: BeautifulSoup Tag
    :return: True or False
    """
    return (
        tag.name == "meta"
        and tag.has_attr("http-equiv")
        and tag.attrs["http-equiv"].lower() == "onion-location"
        and tag.has_attr("content")
    )


def get_onion_location(url: str) -> str | None:
    """Get onion location for a given URL, if it advertises one.

    :param url: The URL to find the onion location for.
    :return: The onion location if one is found, None otherwise.

    .. note::

       Webpages defining `Onion-Location` headers must be served over HTTPS.
       This function will return `None` early for any non-HTTPS `url`.
    """
    if not url.startswith("https://"):
        return None
    with urlopen(url) as request:  # noqa: S310
        onion_location = request.getheader("onion-location", None)
        if onion_location is None:
            soup = BeautifulSoup(request, "lxml")
            # If more than one onion-location exists, we only want the first one.
            onion_location_tag = soup.find(tag_is_onion_location)
            if onion_location_tag:
                onion_location = onion_location_tag.attrs["content"]
    return onion_location


def main(urls: Sequence[str] = tuple(sys.argv[1:])) -> None:
    """Print Onion-Location for provided URLs."""
    for url in urls:
        print(get_onion_location(url))  # noqa: T201


if __name__ == "__main__":
    main(sys.argv[1:])
