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

from unittest import TestCase

from sdk_pure_python.adi_study_watch import SDK

import time

class TestSessionManagerApplication(TestCase):

    @classmethod
    def setUpClass(cls):
        sdk = SDK("COM4", debug=True)
        cls.application = sdk.get_session_manager_application()
        cls.affected_applications = [
            sdk.get_adpd_application(),
            sdk.get_adxl_application(),
            sdk.get_temperature_application(),
            sdk.get_sqi_application(),
            sdk.get_ppg_application(),
            sdk.get_ecg_application(),
        ]

    def test_library_configuration(self):
        x = self.application.write_library_configuration([[0x06, 0x06]])
        assert (x["payload"]["size"] == 1)
        x = self.application.read_library_configuration([0x02, 0x06, 0x07])
        assert (x["payload"]["data"] == [['0x2', '0x0'], ['0x6', '0x6'], ['0x7', '0x64']])

    def test_device_configuration_block(self):
        x = self.application.write_device_configuration_block([[0x10, 0x01], [0x11, 0x02]])
        assert (x["payload"]["size"] == 0)
        x = self.application.read_device_configuration_block()
        assert (x["payload"]["size"] == 2)
        x = self.application.delete_device_configuration_block()
        assert (x["payload"]["size"] == 0)

    def test_sensors(self):
        x = self.application.start_sensor()
        print(x)
        # to check if file created, delete pre-existing xyz named file.
        print("status:")
        a = [app.get_sensor_status for app in self.affected_applications]
        # assert (a == [<bound method ADPDApplication.get_sensor_status of <sdk_pure_python.adi_study_watch.application.adpd_application.ADPDApplication object at 0x000002BB77515810>>, <bound method CommonStream.get_sensor_status of <sdk_pure_python.adi_study_watch.application.adxl_application.ADXLApplication object at 0x000002BB77515540>>, <bound method TemperatureApplication.get_sensor_status of <sdk_pure_python.adi_study_watch.application.temperature_application.TemperatureApplication object at 0x000002BB77515570>>, <bound method CommonStream.get_sensor_status of <sdk_pure_python.adi_study_watch.application.sqi_application.SQIApplication object at 0x000002BB77515510>>, <bound method CommonStream.get_sensor_status of <sdk_pure_python.adi_study_watch.application.ppg_application.PPGApplication object at 0x000002BB77515330>>, <bound method CommonStream.get_sensor_status of <sdk_pure_python.adi_study_watch.application.ecg_application.ECGApplication object at 0x000002BB77515360>>])
        print("CSV logging happening here:")
        b = [app.enable_csv_logging(filename='xyz') for app in self.affected_applications]
        print(b)
        time.sleep(10)
        print("CSV logging stopping here:")
        c = [app.disable_csv_logging() for app in self.affected_applications]
        print(c)
        # to check if file created, check if xyz named file is there or not.
        x = self.application.stop_sensor()
        print(x)
