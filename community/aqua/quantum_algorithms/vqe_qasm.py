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

from qiskit_aqua import Operator, run_algorithm
from qiskit_aqua.input import get_input_instance

pauli_dict = {
    'paulis': [{"coeff": {"imag": 0.0, "real": -1.052373245772859},
                "label": "II"},
               {"coeff": {"imag": 0.0, "real": 0.39793742484318045},
                "label": "ZI"},
               {"coeff": {"imag": 0.0, "real": -0.39793742484318045},
                "label": "ZZ"},
               {"coeff": {"imag": 0.0, "real": 0.18093119978423156},
                "label": "XX"}
               ]
}
algo_input = get_input_instance('EnergyInput')
algo_input.qubit_op = Operator.load_from_dict(pauli_dict)
params = {
    'algorithm': {'name': 'VQE'},
    'optimizer': {'name': 'SPSA'},
    'variational_form': {'name': 'RY', 'depth': 5},
    'backend': {'name': 'qasm_simulator'}
}
result = run_algorithm(params, algo_input)
print(result['energy'])
