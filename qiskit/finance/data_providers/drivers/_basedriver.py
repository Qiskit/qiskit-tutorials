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
This module implements the abstract base class for driver modules
within Qiskit Finance.

To create add-on driver modules subclass the BaseDriver class in this module.
Doing so requires that the required driver interface is implemented.
"""

from abc import ABC, abstractmethod
import copy
from qiskit.aqua.parser import JSONSchema
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class DataType(Enum):
    DAILYADJUSTED = 'Daily (adj)'
    DAILY = 'Daily'


class BaseDriver(ABC):
    """
    Base class for Drivers.

    This method should initialize the module and its configuration, and
    use an exception if a component of the module is available.

    """
    @abstractmethod
    def __init__(self):
        self.check_driver_valid()
        self._configuration = copy.deepcopy(self.CONFIGURATION)
        self._work_path = None

    @property
    def configuration(self):
        """Return driver configuration."""
        return self._configuration

    @classmethod
    def init_from_input(cls, section):
        """
        Initialize via section dictionary.

        Args:
            params (dict): section dictionary

        Returns:
            Driver: Driver object
        """
        pass

    @staticmethod
    def check_driver_valid():
        """Checks if driver is ready for use. Throws an exception if not"""
        pass

    def validate(self, args_dict):
        schema_dict = self.CONFIGURATION.get('input_schema', None)
        if schema_dict is None:
            return

        jsonSchema = JSONSchema(schema_dict)
        schema_property_names = jsonSchema.get_default_section_names()
        json_dict = {}
        for property_name in schema_property_names:
            if property_name in args_dict:
                json_dict[property_name] = args_dict[property_name]

        jsonSchema.validate(json_dict)

    @property
    def work_path(self):
        return self._work_path

    @work_path.setter
    def work_path(self, new_work_path):
        self._work_path = new_work_path

    @abstractmethod
    def run(self):
        pass

    # gets coordinates suitable for plotting
    # it does not have to be overridden in non-abstract derived classes.
    def get_coordinates(self):
        # Coordinates for visualisation purposes
        xc = np.zeros([self.n, 1])
        yc = np.zeros([self.n, 1])
        xc = (np.random.rand(self.n) - 0.5) * 1
        yc = (np.random.rand(self.n) - 0.5) * 1
        #for (cnt, s) in enumerate(self.tickers):
        #xc[cnt, 1] = self.data[cnt][0]
        # yc[cnt, 0] = self.data[cnt][-1]
        return xc, yc

    # it does not have to be overridden in non-abstract derived classes.
    def get_covariance(self):
        if not self._data: return None
        self.cov = np.cov(self._data, rowvar = True)
        return self.cov

    # it does not have to be overridden in non-abstract derived classes.
    def get_similarity_matrix(self):
        if not self.data: return None    
        try:
          import fastdtw
          for ii in range(0, self._n):
            self.rho[ii,ii] = 1.
            for jj in range(ii + 1, self.n):
                thisRho, path = fastdtw.fastdtw(self._data[ii], self._data[jj])
                self.rho[ii, jj] = thisRho
                self.rho[jj, ii] = self.rho[ii, jj]
          self.rho = self.rho / np.nanmax(self.rho)
          for ii in range(0, self.n):
            self.rho[ii,ii] = 1.
        except ImportError:
          print("This requires fastdtw package.")
        return self.rho

    # it does not have to be overridden in non-abstract derived classes.
    def plot(self):  
        #for (cnt, s) in enumerate(self.tickers):
        #    plot(self.data[cnt], grid = True, label=s)
        #plt.legend()
        #plt.title("Evolution of the adjusted closing price")
        #plt.show()
        self.get_covariance()
        self.get_similarity_matrix()
        print("Top: a similarity measure. Bottom: covariance matrix.")
        plt.subplot(211)
        plt.imshow(self.rho)
        plt.subplot(212)
        plt.imshow(self.cov)
        plt.show()     