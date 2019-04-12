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

from qiskit.aqua import Pluggable
from abc import abstractmethod
import copy
from qiskit.aqua import AquaError


class AlgorithmInput(Pluggable):

    _PROBLEM_SET = ['portfoliodiversification', 'portfoliooptimisation']

    @abstractmethod
    def __init__(self):
        super().__init__()
        if 'problems' not in self.configuration or len(self.configuration['problems']) <= 0:
            raise AquaError('Algorithm Input missing or empty configuration problems')

        for problem in self.configuration['problems']:
            if problem not in AlgorithmInput._PROBLEM_SET:
                raise AquaError('Problem {} not in known problem set {}'.format(problem, AlgorithmInput._PROBLEM_SET))

    @property
    def all_problems(self):
        return copy.deepcopy(self._PROBLEM_SET)

    @property
    def problems(self):
        """
        Gets the set of problems that this input form supports
        """
        return self.configuration.problems

    @abstractmethod
    def to_params(self):
        """
        Convert the derived algorithminput class fields to a dictionary where the values are in a
        form that can be saved to json
        Returns:
            Dictionary of input fields
        """
        raise NotImplementedError()

    @abstractmethod
    def from_params(self, params):
        """
        Load the dictionary into the algorithminput class fields. This dictionary being that as
        created by to_params()
        Args:
            params: A dictionary as originally created by to_params()
        """
        raise NotImplementedError()
