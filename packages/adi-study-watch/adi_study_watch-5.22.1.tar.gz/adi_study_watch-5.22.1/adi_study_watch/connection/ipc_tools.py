# ******************************************************************************
# Copyright (c) 2023 Analog Devices, Inc.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
# - Modified versions of the software must be conspicuously marked as such.
# - This software is licensed solely and exclusively for use with
#  processors/products manufactured by or for Analog Devices, Inc.
# - This software may not be combined or merged with other code in any manner
#  that would cause the software to become subject to terms and conditions
#  which differ from those listed here.
# - Neither the name of Analog Devices, Inc. nor the names of its contributors
#  may be used to endorse or promote products derived from this software
#  without specific prior written permission.
# - The use of this software may or may not infringe the patent rights of one
#  or more patent holders.  This license does not release you from the
#  requirement that you obtain separate licenses from these patent holders to
#  use this software.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES, INC. AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# NONINFRINGEMENT, TITLE, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ANALOG DEVICES, INC. OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, DAMAGES ARISING OUT OF
# CLAIMS OF INTELLECTUAL PROPERTY RIGHTS INFRINGEMENT; PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ******************************************************************************

"""
    Interprocess communication tools
"""
import datetime
import queue
import sys
import threading
import time
from typing import Optional, Any, Iterable, List


class BaseThread(threading.Thread):
    """
        Extends Thread functionality by adding Event to gracefully shut down the thread
        and start delay.
    """

    TIMESTAMP_TO_MILLISECONDS = 1e3

    def __init__(self):
        threading.Thread.__init__(self, target=self._run)
        self._is_running: threading.Event = threading.Event()
        self.start_delay: int = 0

    def _run(self):

        if self.start_delay > 0:
            time.sleep(self.start_delay)
        while self._is_running.is_set():
            self.loop()

    def start(self, start_delay: int = 0):
        self._is_running.set()
        self.start_delay = start_delay
        super().start()

    def stop(self):
        self._is_running.clear()

    def loop(self):
        raise NotImplemented()

    def is_running(self) -> bool:
        return self._is_running.is_set()

    @staticmethod
    def get_ts(utc: bool = True) -> int:

        if utc:
            dt = datetime.datetime.now(datetime.timezone.utc)
            utc_time = dt.replace(tzinfo=datetime.timezone.utc)
            return int(utc_time.timestamp() * BaseThread.TIMESTAMP_TO_MILLISECONDS)

        return int(time.time() * BaseThread.TIMESTAMP_TO_MILLISECONDS)


class FifoQueue:
    """
        Thread safe FIFO queue implementation

    """

    def __init__(self, maxsize: int = 0):

        self.max_size: int = maxsize
        self._internal_queue: queue.Queue = queue.Queue(maxsize)
        self._q_lock: threading.Lock = threading.Lock()

    def push(self, item: Any) -> Optional[Any]:
        """
            Push one item to FIFO queue
            return: removed older items list if queue is full
        """
        _e: Optional[Any] = None
        with self._q_lock:
            if self._internal_queue.full():
                _e = self._internal_queue.get()
            self._internal_queue.put(item)
        return _e

    def push_all(self, item: Iterable) -> List[Any]:
        """
            Push a list of items to queue as separated.
            If internal queue is full, remove the oldest item.
            return: a list of removed items if any
        """
        _removed: List[Any] = []
        with self._q_lock:
            for _i in item:
                if self._internal_queue.full():
                    _removed.append(self._internal_queue.get())
                self._internal_queue.put(_i)
        return _removed

    def pop(self, timeout: int = 0) -> Optional[Any]:
        """
            Pop one item from FIFO. Will return immediately if there is an item in the queue,
            block and wait with timeout until an item is available in the queue.

            Return none if timeout or no items in the queue.
        """
        with self._q_lock:
            if not self._internal_queue.empty():
                return self._internal_queue.get(block=timeout > 0, timeout=timeout)
        return None

    def pop_all(self, timeout: int = 0, count: int = sys.maxsize, wait_all: bool = False) -> Optional[List[Any]]:
        """
            Pop desired count of items form queue, with timeout or block until all are available.
        """

        result: Optional[List[Any]] = []
        start_time: int = int(time.time())

        # non blocking
        if timeout == 0:
            with self._q_lock:
                if wait_all and self._internal_queue.qsize() >= count:
                    while len(result) < count:
                        result.append(self._internal_queue.get())
                    return result

                if not wait_all:
                    while not self._internal_queue.empty() and len(result) < count:
                        result.append(self._internal_queue.get())
                    return result

            if wait_all:
                return None

        # blocking with timeout
        while int(time.time()) - start_time < timeout:
            with self._q_lock:

                if wait_all and self._internal_queue.qsize() >= count:
                    while len(result) < count:
                        result.append(self._internal_queue.get())
                    return result

                if not wait_all:
                    while not self._internal_queue.empty() and len(result) < count:
                        result.append(self._internal_queue.get())
            time.sleep(1)

        return result if len(result) > 0 else None

    def clear(self) -> None:
        """
            Remove all items from queue
        """
        with self._q_lock:
            self._internal_queue = queue.Queue(self.max_size)

    def empty(self) -> bool:
        """
            Check if queue is empty
        """
        with self._q_lock:
            return self._internal_queue.empty()
