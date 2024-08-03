.. SPDX-FileCopyrightText: © 2024 Frederik “Freso” S. Olesen
.. SPDX-License-Identifier: AGPL-3.0-or-later

================
 Onion-Location
================

Python library for discovering `Onion-Location`_ HTTP headers.

.. _`Onion-Location`: https://community.torproject.org/onion-services/advanced/onion-location/

-------
 Usage
-------

>>> from onion_location import get_onion_location
>>> get_onion_location("https://www.torproject.org/")
'http://2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion/index.html'
