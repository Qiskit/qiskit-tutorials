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

from qiskit_aqua_chemistry import AquaChemistry

# Input dictionary to configure Qiskit Aqua Chemistry for the chemistry problem.
aqua_chemistry_dict = {
    'driver': {'name': 'PYSCF'},
    'PYSCF': {'atom': 'Li .0 .0 -0.8; H .0 .0 0.8', 'basis': 'sto3g'},
    'operator': {'name': 'hamiltonian', 'qubit_mapping': 'parity',
                 'two_qubit_reduction': True, 'freeze_core': True,
                 'orbital_reduction': [-3, -2]},
    'algorithm': {'name': 'VQE'},
    'optimizer': {'name': 'COBYLA', 'maxiter': 10000},
    'variational_form': {'name': 'UCCSD'},
    'initial_state': {'name': 'HartreeFock'}
}

solver = AquaChemistry()
result = solver.run(aqua_chemistry_dict)
print(result['energy'])
