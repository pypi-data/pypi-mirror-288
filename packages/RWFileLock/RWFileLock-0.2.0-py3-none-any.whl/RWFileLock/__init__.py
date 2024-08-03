#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf-8

# SPDX-License-Identifier: LGPL-2.1-or-later
# RWFileLock: Readers / writers file lock Python helper class
# Copyright 2020-2024 Barcelona Supercomputing Center (BSC), Spain
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA

from __future__ import absolute_import

from .rw_file_lock import (
    LockError,
    RWFileLock,
)

# https://www.python.org/dev/peps/pep-0396/
__version__ = version = "0.2.0"
__author__ = "José M. Fernández <https://orcid.org/0000-0002-4806-5140>"
__copyright__ = "© 2020-2024 Barcelona Supercomputing Center (BSC), ES"
__license__ = "LGPLv2"

__url__ = "https://github.com/inab/RWFileLock"
__official_name__ = "RWFileLock"

__all__ = [
    "__version__",
    "LockError",
    "RWFileLock",
]
