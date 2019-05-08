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

import qiskit.chemistry

# An example of using a loop to vary inter-atomic distance. A dictionary is
# created outside the loop, but inside the loop the 'atom' value is updated
# with a new molecular configuration. The molecule is H2 and its inter-atomic distance
# i.e the distance between the two atoms, is altered from 0.5 to 1.0. Each atom is
# specified by x, y, z coords and the atoms are set on the z-axis, equidistant from
# the origin, and updated by d inside the loop where the molecule string has this value
# substituted by format(). Note the negative sign preceding the first format
# substitution point i.e. the {} brackets
#
input_dict = {
    'driver': {'name': 'PYSCF'},
    'PYSCF': {'atom': None, 'unit': 'Angstrom', 'charge': 0, 'spin': 0, 'basis': 'sto3g'},
    'algorithm': {'name': 'ExactEigensolver'},
}
molecule = 'H .0 .0 -{0}; H .0 .0 {0}'
for i in range(21):
    d = (0.5 + i * 0.5 / 20) / 2
    input_dict['PYSCF']['atom'] = molecule.format(d)
    solver = qiskit.chemistry.QiskitChemistry()
    result = solver.run(input_dict)
    print('{:.4f} : {}'.format(d * 2, result['energy']))
