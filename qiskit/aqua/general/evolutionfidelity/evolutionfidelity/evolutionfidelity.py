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
Qiskit Aqua library. Algorithms are designed to be dynamically discovered within
Qiskit Aqua. For this the entire parent directory 'evolutionfidelity' should
be moved under the 'qiskit/aqua' directory. The current demonstration notebook
shows how to explicitly register the algorithm and works without re-locating this
code. The former automatic discovery does however allow the algorithm to be found
and seen in the UI browser, and selected from the GUI when choosing an algorithm.
"""

import logging

import numpy as np
from qiskit import QuantumRegister
from qiskit.quantum_info import state_fidelity

from qiskit.aqua.algorithms import QuantumAlgorithm
from qiskit.aqua import AquaError, Pluggable, PluggableType, get_pluggable_class

logger = logging.getLogger(__name__)


class EvolutionFidelity(QuantumAlgorithm):
    """The Tutorial Sample EvolutionFidelity algorithm."""
    PROP_EXPANSION_ORDER = 'expansion_order'

    """
    A configuration dictionary defines the algorithm to QISKIt Aqua. It can contain
    the following though this sample does not have them all.

    name: Is the registered name and will be used as the case-sensitive key to load an instance
    description: As it implies a brief description of algorithm
    classical: True if purely a classical algorithm that does not need a quantum backend
    input_schema: A json schema detailing the configuration variables of this entity.
                  Each variable as a type, and can be given default, minimum etc. This conforms
                  to JSON Schema which can be consulted for for detail. The existing algorithms
                  and other pluggable entities may also be helpful to refer to.
    problems: A list of problems the algorithm can solve
    depends: A list of dependent object types
    defaults: A list of configurations for the dependent objects. May just list names if the
              dependent's defaults are acceptable
    """
    CONFIGURATION = {
        'name': 'EvolutionFidelity',
        'description': 'Sample Demo EvolutionFidelity Algorithm for Quantum Systems',
        'input_schema': {
            '$schema': 'http://json-schema.org/schema#',
            'id': 'evolution_fidelity_schema',
            'type': 'object',
            'properties': {
                PROP_EXPANSION_ORDER: {
                    'type': 'integer',
                    'default': 1,
                    'minimum': 1
                },
            },
            'additionalProperties': False
        },
        'problems': ['eoh'],
        'depends': [
            {
                'pluggable_type': 'initial_state',
                'default': {
                    'name': 'ZERO',
                }
            },
        ]
    }

    """
    If directly use these objects programmatically then the constructor is more convenient to call
    than init_params. init_params itself uses this to do the actual object initialization.
    """

    def __init__(self, operator, initial_state, expansion_order=1):
        self.validate(locals())
        super().__init__()
        self._operator = operator
        self._initial_state = initial_state
        self._expansion_order = expansion_order
        self._ret = {}

    """
    init_params is called via run_algorithm. The params contain all the configuration settings
    of the objects. algo_input contains data computed from above for the algorithm. A simple
    algorithm may have all its data in configuration params such that algo_input is None
    """
    @classmethod
    def init_params(cls, params, algo_input):
        """
        Initialize via parameters dictionary and algorithm input instance.

        Args:
            params: parameters dictionary
            algo_input: EnergyInput instance
        """
        if algo_input is None:
            raise AquaError("EnergyInput instance is required.")

        operator = algo_input.qubit_op

        evolution_fidelity_params = params.get(Pluggable.SECTION_KEY_ALGORITHM)
        expansion_order = evolution_fidelity_params.get(EvolutionFidelity.PROP_EXPANSION_ORDER)

        # Set up initial state, we need to add computed num qubits to params
        initial_state_params = params.get(Pluggable.SECTION_KEY_INITIAL_STATE)
        initial_state_params['num_qubits'] = operator.num_qubits
        initial_state = get_pluggable_class(PluggableType.INITIAL_STATE,
                                            initial_state_params['name']).init_params(params)

        return cls(operator, initial_state, expansion_order)

    """
    Once the algorithm has been initialized then run is called to carry out the computation
    and the result is returned as a dictionary.

    E.g., the `_run` method is required to be implemented for an algorithm.
    """

    def _run(self):
        evo_time = 1
        # get the groundtruth via simple matrix * vector
        state_out_exact = self._operator.evolve(self._initial_state.construct_circuit('vector'), evo_time, 'matrix', 0)

        qr = QuantumRegister(self._operator.num_qubits, name='q')
        circuit = self._initial_state.construct_circuit('circuit', qr)
        circuit += self._operator.evolve(
            None, evo_time, 'circuit', 1,
            quantum_registers=qr,
            expansion_mode='suzuki',
            expansion_order=self._expansion_order
        )

        result = self._quantum_instance.execute(circuit)
        state_out_dynamics = np.asarray(result.get_statevector(circuit))

        self._ret['score'] = state_fidelity(state_out_exact, state_out_dynamics)

        return self._ret
