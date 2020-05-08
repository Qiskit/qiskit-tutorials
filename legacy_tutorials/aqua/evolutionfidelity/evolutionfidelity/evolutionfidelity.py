# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""
The Fidelity of Quantum Evolution.
This is a simple tutorial example to show how to build an algorithm to extend
Qiskit Aqua library.
"""

import logging

import numpy as np
from qiskit import QuantumRegister
from qiskit.quantum_info import state_fidelity
from qiskit.aqua.algorithms import QuantumAlgorithm
from qiskit.aqua.operators import op_converter

logger = logging.getLogger(__name__)


class EvolutionFidelity(QuantumAlgorithm):

    CONFIGURATION = {
    }

    def __init__(self, operator, initial_state, expansion_order=1):
        self.validate(locals())
        super().__init__()
        self._operator = operator
        self._initial_state = initial_state
        self._expansion_order = expansion_order
        self._ret = {}

    """
    Once the algorithm has been initialized then run is called to carry out the computation
    and the result is returned as a dictionary.

    E.g., the `_run` method is required to be implemented for an algorithm.
    """

    def _run(self):
        evo_time = 1
        # get the groundtruth via simple matrix * vector
        state_out_exact = op_converter.to_matrix_operator(self._operator).evolve(
            self._initial_state.construct_circuit('vector'), evo_time, num_time_slices=1)

        qr = QuantumRegister(self._operator.num_qubits, name='q')
        circuit = self._initial_state.construct_circuit('circuit', qr)
        circuit += self._operator.evolve(
            None, evo_time, 1,
            quantum_registers=qr,
            expansion_mode='suzuki',
            expansion_order=self._expansion_order
        )
        result = self._quantum_instance.execute(circuit)
        state_out_dynamics = np.asarray(result.get_statevector(circuit))

        self._ret['score'] = state_fidelity(state_out_exact, state_out_dynamics)

        return self._ret
