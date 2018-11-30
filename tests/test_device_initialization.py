# Copyright 2018 Carsten Blank

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Unit tests for the :mod:`pennylane_qiskit` device initialization
"""

import logging as log
import unittest

from pennylane import DeviceError

from defaults import pennylane as qml, BaseTest, TOKEN
from pennylane_qiskit import IbmQQiskitDevice

log.getLogger('defaults')


class DeviceInitialization(BaseTest):
    """test aspects of the device initialization.
    """

    num_subsystems = 4
    devices = None

    def test_ibm_no_token(self):
        if self.args.device == 'ibmq_qasm_simulator' or self.args.device == 'all':
            self.assertRaises(ValueError, IbmQQiskitDevice, wires=self.num_subsystems)

    def test_log_verbose(self):
        dev = IbmQQiskitDevice(wires=self.num_subsystems, log=True, ibmqx_token=TOKEN)
        self.assertEqual(dev.kwargs['log'], True)
        self.assertEqual(dev.kwargs['log'], dev.kwargs['verbose'])

    def test_shots(self):
        if self.args.device == 'ibmq_qasm_simulator' or self.args.device == 'all':
            shots = 5
            dev1 = IbmQQiskitDevice(wires=self.num_subsystems, shots=shots, ibmqx_token=TOKEN)
            self.assertEqual(shots, dev1.shots)
            self.assertEqual(shots, dev1.kwargs['num_runs'])

            dev2 = IbmQQiskitDevice(wires=self.num_subsystems, num_runs=shots, ibmqx_token=TOKEN)
            self.assertEqual(shots, dev2.shots)
            self.assertEqual(shots, dev2.kwargs['num_runs'])

            dev2 = IbmQQiskitDevice(wires=self.num_subsystems, shots=shots+2, num_runs=shots, ibmqx_token=TOKEN)
            self.assertEqual(shots, dev2.shots)
            self.assertEqual(shots, dev2.kwargs['num_runs'])

    def test_initiatlization_via_pennylane(self):
        for short_name in [
                'qiskit.aer',
                'qiskit.ibm'
        ]:
            try:
                dev = dev = qml.device(short_name, wires=2, ibmqx_token=TOKEN)
            except DeviceError:
                raise Exception("This test is expected to fail until pennylane-qiskit is installed.")


if __name__ == '__main__':
    print('Testing PennyLane qiskit Plugin version ' + qml.version() + ', device initialization.')
    # run the tests in this file
    suite = unittest.TestSuite()
    for t in (DeviceInitialization, ):
        ttt = unittest.TestLoader().loadTestsFromTestCase(t)
        suite.addTests(ttt)

    unittest.TextTestRunner().run(suite)