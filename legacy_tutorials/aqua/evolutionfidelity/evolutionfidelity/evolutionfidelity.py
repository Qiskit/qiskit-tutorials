# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""
The Fidelity of Quantum Evolution.
This is a simple tutorial example to show how to build an algorithm to extend
Qiskit Aqua library.
"""

from typing import Optional, Union
import logging

import numpy as np
from qiskit import QuantumRegister
from qiskit.quantum_info import state_fidelity
from qiskit.providers import BaseBackend
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import QuantumAlgorithm
from qiskit.aqua.operators import op_converter
from qiskit.aqua.components.initial_states import InitialState
from qiskit.aqua.operators.legacy import LegacyBaseOperator

logger = logging.getLogger(__name__)


class EvolutionFidelity(QuantumAlgorithm):

    def __init__(self,
                 operator: LegacyBaseOperator,
                 initial_state: InitialState,
                 expansion_order: int = 1,
                 quantum_instance: Optional[Union[QuantumInstance, BaseBackend]] = None) -> None:
        super().__init__(quantum_instance)
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
