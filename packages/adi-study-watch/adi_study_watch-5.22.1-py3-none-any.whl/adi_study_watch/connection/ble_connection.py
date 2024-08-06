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
    Implements ConnectionInterface for NRF BLE UART service using host device built in BLE
"""
import logging
import sys
import threading
import time
from asyncio import Task
from typing import Optional

from .ipc_tools import BaseThread, FifoQueue
from .connection_interface import ConnectionInterface
from bleak import BleakClient, BleakGATTCharacteristic
import asyncio

logger = logging.getLogger(__name__)

logi = logger.info
logw = logger.warning
loge = logger.error


class NrfUartBleConnection(ConnectionInterface, BaseThread):
    """
        Non-blocking write/read ble  communication
        interface implementation.

        There are two FIFO queues, one for TX and another for RX.
        When write is called, data are pushed to write (TX) queue,
        write thread will peek and send.

        When the data are received, ble characteristic callback
        will push the data to a read (RX) queue, and read() function
        will return them

    """

    # NRF defined constants
    READ_DESCRIPTOR_UUID: str = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
    WRITE_CHARACTERISTIC_UUID: str = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
    READ_CHARACTERISTIC_UUID: str = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    RX_QUEUE_MAX_SIZE = 100
    TX_QUEUE_MAX_SIZE = 100

    def __init__(self, ble_address: str, *args, **kwargs):
        BaseThread.__init__(self)
        ConnectionInterface.__init__(self, *args, **kwargs)
        self._is_connected: threading.Event = threading.Event()
        self.ble_address: str = ble_address
        self.write_queue: FifoQueue = FifoQueue(maxsize=NrfUartBleConnection.TX_QUEUE_MAX_SIZE)
        self.read_queue: FifoQueue = FifoQueue(maxsize=NrfUartBleConnection.RX_QUEUE_MAX_SIZE)
        self.read_task: Optional[Task] = None
        self.async_loop = None
        self._is_opened: threading.Event = threading.Event()

    def read(self, size=1) -> bytes:
        """
            Read data if any, otherwise immediately return empty. Nor blocking mode
        :param size: number of bytes to read, default 1
        :return: bytes read or empty

        """
        _d = self.read_queue.pop_all(count=size, wait_all=False)
        if _d is None:
            return b''
        return bytes(_d)

    def write(self, data) -> int:
        """
            Write data to BLE, return count written. Non-blocking mode
        :param data: data to write to BLE
        :return: number of bytes written to internal queue, not actually sent
        """
        self.write_queue.push_all(data)
        return len(data)

    def close(self) -> None:
        """
            Stop internal processes and close connection
        :return: none
        """
        logi('NrfUartBleConnection.close::>> CLOSE ')
        if not self._is_opened.is_set():
            logw('NrfUartBleConnection.close::>> Already closed')
            return

        self._is_opened.clear()
        self._is_connected.clear()
        self.stop()

        try:
            logi(f'NrfUartBleConnection.close::>> Running loop {asyncio.get_running_loop()}')
            for task in asyncio.all_tasks():
                logi(f'NrfUartBleConnection.close::>> Cancel task {task}')
                task.cancel()
            logi(f'NrfUartBleConnection.close::>> Running loop {asyncio.get_running_loop()}')
        except Exception as e:
            logw(f'NrfUartBleConnection.close::>> Close exception: {e}')
        logi("NrfUartBleConnection.close::>> Connection closed!")

    def handle_disconnect(self, client: BleakClient):
        """
            Bleak Disconnect callback

        """
        logi(f"NrfUartBleConnection.handle_disconnect::>> Device was disconnected, goodbye: {client}")
        self.close()

    def handle_rx(self, _: BleakGATTCharacteristic, data: bytearray):
        """
            Bleak RX callback
        """
        self.read_queue.push_all(data)

    async def ble_service_task(self):
        """
            BLE asyncio communication task that connects, and waits for messages in TX queue
        :return: none
        """

        logi(f'NrfUartBleConnection.ble_service_task::>> Connecting to device {self.ble_address}')
        try:
            async with BleakClient(self.ble_address, disconnected_callback=self.handle_disconnect) as client:

                await client.start_notify(NrfUartBleConnection.READ_CHARACTERISTIC_UUID, self.handle_rx)

                nus = client.services.get_service(NrfUartBleConnection.READ_DESCRIPTOR_UUID)
                tx_char = nus.get_characteristic(NrfUartBleConnection.WRITE_CHARACTERISTIC_UUID)

                self._is_connected.set()
                logi(f'NrfUartBleConnection.ble_service_task::>> Connected to client {client}')
                while self.is_running() and client.is_connected:
                    if not self.write_queue.empty():
                        _d = self.write_queue.pop_all(count=sys.maxsize, wait_all=False)
                        await client.write_gatt_char(tx_char, bytearray(_d))
                    else:
                        await asyncio.sleep(0.01)
                if client.is_connected:
                    logi(f'NrfUartBleConnection.ble_service_task::>> Stop communication with {client}, '
                         f'disconnecting ...')
                    await client.disconnect()

                self._is_connected.clear()
                logi(f'NrfUartBleConnection.ble_service_task::>> Communication with {client} stopped, close connection')
                self.close()

        except Exception as e:
            loge(f'NrfUartBleConnection.ble_service_task::>> ble_service_task exception: - {e}')
            self.close()

        logi('NrfUartBleConnection.ble_service_task::>> BLE Task stopped')

    def open(self, timeout: int = 0) -> bool:
        """
            Open connection with optional timeout
        :param timeout: time out to wait before fail. If zero, will wait forever
        :return: True if connection is successful
        :note: By default, this function will block forever
        """
        self.start(start_delay=0)
        logi('NrfUartBleConnection.open::>> Open ...')
        try:
            start_time: int = int(time.time())
            while self.is_running() and not self.is_connected():
                time.sleep(1)
                if 0 < timeout <= int(time.time()) - start_time:
                    break
            self._is_opened.set()

            return self.is_connected()
        except Exception as ex:
            loge(f'NrfUartBleConnection.open::>> Failed to connect {ex}')

        return False

    def loop(self):
        """
            Wraps asyncio call
        :return: none
        """
        try:
            self.async_loop = asyncio.new_event_loop()
            self.async_loop.run_until_complete(self.ble_service_task())
        except asyncio.CancelledError as e:
            loge(e)

        self.close()

    def cancel_read(self) -> None:
        """
            Not blocking when read
        :return: none
        """
        pass

    def is_connected(self) -> bool:
        """
            Check if device is connected (communication channel is open)
            :return: True or false
        """
        return self._is_connected.is_set()
