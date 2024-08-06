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
    Connection Interface definition, that should be implemented to allow SDK to
    communicate with custom interfaces (Serial, BLE, TCP/IP, etc)

"""
import abc
import enum


class CommunicationMode(enum.IntEnum):
    """
        Select one of the communication modes.
    """
    SerialOrDongle = 0  # Use serial port or ble dongle
    BleNative = 1  # Use built in computer BLE


class ConnectionInterface(abc.ABC):
    """
        Interface to allow read/write to a device.
        This is an abstract class, that cannot be instantiated directly, and needs an implementation.
    """

    def __init__(self, *args, **kwargs):
        """
            Init witg arguments and keyword-arguments
        """
        pass

    def read(self, size=1) -> bytes:
        """
            Read one byte by default. Blocking/Nonblocking Behaviour depends on the implementation
            return: bytes read
        """
        pass

    def write(self, data) -> int:
        """
            Write data. Blocking/Nonblocking Behaviour depends on the implementation
            return: amount of bytes successfully written
        """
        pass

    def close(self) -> None:
        """
            Close connection
        """
        pass

    def open(self) -> None:
        """
            Open connection
        """
        pass

    def cancel_read(self) -> None:
        """
            Cancel current read operation. Useful when in blocking mode
        """
        pass

    def is_connected(self) -> bool:
        """
            Check if communication interface is connected or opened
        :return: True - connected or opened
        """
