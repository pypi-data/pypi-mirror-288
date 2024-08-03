#!/usr/bin/env python3
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

import os
import contextlib
import tempfile
import fcntl

from typing import (
    cast,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from typing import (
        Iterator,
        Optional,
        Union,
    )

    from typing_extensions import (
        Protocol,
    )

    class FilenoProtocol(Protocol):
        def fileno(self) -> "int":
            ...


class LockError(Exception):
    def __init__(self, message: "str"):
        super().__init__(message)


class RWFileLock(object):
    def __init__(self, filename: "Union[str, os.PathLike[str], int, FilenoProtocol]"):
        if hasattr(filename, "fileno") and callable(getattr(filename, "fileno")):
            self.lock_fd = filename.fileno()
            self.should_close = False
        elif isinstance(filename, int):
            self.lock_fd = filename
            self.should_close = False
        else:
            self.lock_fd = os.open(
                cast("Union[str, os.PathLike[str]]", filename),
                (os.O_RDWR | os.O_CREAT),
                mode=0o700,
            )
            self.should_close = True

        self.isLocked = False
        self.isShareLock = False

    def r_lock(self) -> "None":
        if self.isLocked and self.isShareLock:
            raise LockError("Already locked by ourselves")

        try:
            fcntl.lockf(self.lock_fd, (fcntl.LOCK_SH | fcntl.LOCK_NB))
            self.isLocked = True
            self.isShareLock = True
        except IOError:
            raise LockError("Already locked by others")

    def r_blocking_lock(self) -> "None":
        if self.isLocked and self.isShareLock:
            raise LockError("Already locked by ourselves")

        fcntl.lockf(self.lock_fd, fcntl.LOCK_SH)
        self.isLocked = True
        self.isShareLock = True

    def w_lock(self) -> "None":
        if self.isLocked and not self.isShareLock:
            raise LockError("Already locked by ourselves")

        try:
            fcntl.lockf(self.lock_fd, (fcntl.LOCK_EX | fcntl.LOCK_NB))
            self.isLocked = True
            self.isShareLock = False
        except IOError:
            raise LockError("Already locked by others")

    def w_blocking_lock(self) -> "None":
        if self.isLocked and not self.isShareLock:
            raise LockError("Already locked by ourselves")

        try:
            fcntl.lockf(self.lock_fd, fcntl.LOCK_EX)
            self.isLocked = True
            self.isShareLock = False
        except OSError:
            raise LockError("Read only file descriptor?")

    def unlock(self) -> "None":
        if self.isLocked:
            try:
                fcntl.lockf(self.lock_fd, fcntl.LOCK_UN)
            except IOError:
                raise LockError("Already locked by others")
            finally:
                self.isLocked = False
        else:
            raise LockError("No lock was held")

    @contextlib.contextmanager
    def shared_lock(self) -> "Iterator[None]":
        self.r_lock()
        try:
            yield
        finally:
            self.unlock()

    @contextlib.contextmanager
    def shared_blocking_lock(self) -> "Iterator[None]":
        try:
            self.r_lock()
            yield
        finally:
            self.unlock()

    @contextlib.contextmanager
    def exclusive_lock(self) -> "Iterator[None]":
        self.w_lock()
        try:
            yield
        finally:
            self.unlock()

    @contextlib.contextmanager
    def exclusive_blocking_lock(self) -> "Iterator[None]":
        try:
            self.w_blocking_lock()
            yield
        finally:
            self.unlock()

    def __del__(self) -> "None":
        if self.should_close:
            try:
                os.close(self.lock_fd)
            except:
                pass


if __name__ == "__main__":
    lock = RWFileLock("/tmp/rwfilelock.lock")
    # fH = open("/etc/passwd", mode="r")
    # lock = RWFileLock(fH)

    import datetime
    import sys
    import time

    print(f"[{datetime.datetime.now().isoformat()}] Trying getting lock {os.getpid()}")

    sys.stdout.flush()
    try:
        if len(sys.argv) == 3:
            lock.r_blocking_lock()
            print(f"[{datetime.datetime.now().isoformat()}] Got shlock {os.getpid()}")
            time.sleep(5)
            print(
                f"[{datetime.datetime.now().isoformat()}] Trying to switch exlock {os.getpid()}"
            )
            lock.w_blocking_lock()
            print(f"[{datetime.datetime.now().isoformat()}] Got exlock {os.getpid()}")
            time.sleep(3)
            print(
                f"[{datetime.datetime.now().isoformat()}] Releasing exlock {os.getpid()}"
            )
            lock.unlock()
        elif len(sys.argv) == 2:
            with lock.exclusive_lock():
                print(
                    f"[{datetime.datetime.now().isoformat()}] Got exlock {os.getpid()}"
                )

                time.sleep(10)
                print(
                    f"[{datetime.datetime.now().isoformat()}] Releasing exlock {os.getpid()}"
                )
        else:
            with lock.shared_lock():
                print(
                    f"[{datetime.datetime.now().isoformat()}] Got shlock {os.getpid()}"
                )

                time.sleep(7)
                print(
                    f"[{datetime.datetime.now().isoformat()}] Releasing shlock {os.getpid()}"
                )
    except LockError:
        print(
            f"[{datetime.datetime.now().isoformat()}] Unable to get lock {os.getpid()}"
        )
