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

from datasets import *
from qiskit_aqua.utils import split_dataset_to_data_and_labels
from qiskit_aqua.input import get_input_instance
from qiskit_aqua import run_algorithm

sample_Total, training_input, test_input, class_labels = \
    ad_hoc_data(training_size=10, test_size=10, n=2,  # 2 is the dimension of each data point
                gap=0.3, PLOT_DATA=False)


datapoints, class_to_label = split_dataset_to_data_and_labels(test_input)

params = {
    'problem': {'name': 'svm_classification', 'random_seed': 10598},
    'algorithm': {
        'name': 'QSVM.Kernel'
    },
    'backend': {'name': 'qasm_simulator', 'shots': 1024},
    'feature_map': {'name': 'SecondOrderExpansion', 'depth': 2, 'entanglement': 'linear'}
}

algo_input = get_input_instance('SVMInput')
algo_input.training_dataset = training_input
algo_input.test_dataset = test_input
algo_input.datapoints = datapoints[0]  # 0 is data, 1 is labels

result = run_algorithm(params, algo_input)
print(result)

# import matplotlib.pyplot as plt
# kernel_matrix = result['training_kernel_matrix']
# img = plt.imshow(np.asmatrix(kernel_matrix),interpolation='nearest',origin='upper',cmap='bone_r')
# plt.show()
