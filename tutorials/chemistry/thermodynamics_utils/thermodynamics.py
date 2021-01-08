# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2020, 2020
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""
This module implements fundamental thermodynamics of a system.
Functions/classes here require a partition function argument which contains
the properties and energies of the underlying molecule.
"""

from functools import partial

import numpy as np
import qiskit.chemistry.constants as const
from thermodynamics_utils.partition_function import PartitionFunctionBase


# Note: Default units are Joules per mol (per Kelvin), since we
#       work in Joules and (by default) multiply by N_A.
#       Use 'scale_factor' to rescale (the Joules value) if needed.

def helmholtz_free_energy(partition, temperature, scale_factor=const.N_A):
    """
    Calculates the Helmholtz free energy for a given partition functions.
    Default units are Joules *per mol*, since the default scaling is the
    Avogadro's number.
    Use 'scale_factor' to rescale (the Joules value) if needed.

    Args:
        partition (callable) : Partition function.
        temperature (float or numpy.array) : Temperature(s).
        scale_factor (float, optional) : Scaling of the energy (in Joules).
                 The default is Avogadro's number for Joules per mol.

    Returns:
        float or numpy.array : The Helmholtz free energy for a
        given partition function at the given temperature(s) scaled
        appropriately.
    """
    formula = -np.log(partition(temperature)) * temperature * const.KB_J_PER_K
    return scale_factor * formula


def thermodynamic_energy(partition, temperature,
                         scale_factor=const.N_A, *, d_t=1E-4):
    """
    Calculates the Thermodynamic energy for a given partition function at
    given temperature value(s).
    Default units are Joules *per mol*, since the default scaling is the
    Avogadro's number.
    Use 'scale_factor' to rescale (the Joules value) if needed.

    Args:
        partition (callable) : Partition function.
        temperature (float or numpy.array) : Temperature(s).
        scale_factor (float, optional) : Scaling of the energy (in Joules).
                 The default is Avogadro's number for Joules per mol.
        d_t (float, optional) : Shift for numerical derivative calculation.
        Used only if the passed callable is not of type DifferentiableFunction.

    Returns:
        float or numpy.array : The Thermodynamic energy for a given partition
        function at the given temperature(s) scaled appropriately.
    """
    formula = (
        (np.log(partition(temperature + d_t)) -
         np.log(partition(temperature - d_t)))
        / (2 * d_t) * temperature ** 2 * const.KB_J_PER_K)
    # TODO: Find a better way! isinstance does not always work.
    if 'DifferentiableFunction' in str(type(partition)):
        formula = (partition.D(temperature) / partition(temperature)
                   * temperature ** 2 * const.KB_J_PER_K)
    return scale_factor * formula


# In Joules (per mol) per Kelvin
def entropy(partition, temperature, scale_factor=const.N_A):
    """
    Calculates the entropy of a system for a given partition function at
    given temperature value(s).
    Default units are Joules *per mol* per Kelvin, since the default
    scaling is the Avogadro's number.
    Use 'scale_factor' to rescale (the Joules per Kelvin value) if needed.

    Args:
        partition (callable) : Partition function.
        temperature (float or numpy.array) : Temperature(s).
        scale_factor (float, optional) : Scaling of the entropy
                                         (in Joules per Kelvin).
        The default is Avogadro's number for Joules per mol per Kelvin.

    Returns:
        float or numpy.array : The entropy for a given partition function at
        the given temperature(s) scaled appropriately.
    """

    formula = (thermodynamic_energy(partition, temperature, 1.0) -
               helmholtz_free_energy(partition, temperature, 1.0)
               ) / temperature
    return scale_factor * formula


def enthalpy(partition, temperature, scale_factor=const.N_A):
    """
    Calculates the enthalpy of a system for a given partition function at
    given temperature value(s).
    Default units are Joules *per mol*, since the default
    scaling is the Avogadro's number.
    Use 'scale_factor' to rescale (the Joules value) if needed.

    Args:
        partition (callable) : Partition function.
        temperature (float or numpy.array) : Temperature(s).
        scale_factor (float, optional) : Scaling of the energy (in Joules).
                 The default is Avogadro's number for Joules per mol.

    Returns:
        float or numpy.array : The enthalpy for a given partition function at
        the given temperature(s) scaled appropriately.
    """
    # Note, scaling in the formula is 1.0 and not the given scale factor,
    #       as the user defined scale_factor will be applied below.
    formula = (thermodynamic_energy(partition, temperature, 1.0) +
               temperature * const.KB_J_PER_K)
    return scale_factor * formula


def gibbs_free_energy(partition, temperature, scale_factor=const.N_A):
    """
    Calculates the Gibbs free energy for a given partition function at
    given temperature value(s).
    Default units are Joules *per mol*, since the default
    scaling is the Avogadro's number.
    Use 'scale_factor' to rescale (the Joules value) if needed.

    Args:
        partition (callable) : Partition function.
        temperature (float or numpy.array) : Temperature(s).
        scale_factor (float, optional) : Scaling of the energy (in Joules).
                 The default is Avogadro's number for Joules per mol.

    Returns:
        float or numpy.array : The Gibbs free energy for a given partition
        functions at the given temperature(s) scaled appropriately.
    """
    # Note, scaling in the formula is 1.0 and not the given scale factor,
    #       as the user defined scale_factor will be applied below.
    formula = (enthalpy(partition, temperature, 1.0) -
               temperature * entropy(partition, temperature, 1.0))
    return scale_factor * formula


# In Joules per Kelvin
def constant_volume_heat_capacity(partition, temperature,
                                  scale_factor=const.N_A, *, d_t=1E-4):
    """
    Calculates the Constant-volume Heat capacity for a given partition
    function at given temperature value(s).
    Default units are Joules *per mol* per Kelvin, since the default
    scaling is the Avogadro's number.
    Use 'scale_factor' to rescale (the Joules per Kelvin value) if needed.

    Args:
        partition (callable) : Partition function.
        temperature (float or numpy.array) : Temperature(s).
        scale_factor (float, optional) : Scaling of the energy
                                         (in Joules per Kelvin).
        The default is Avogadro's number for Joules per mol per Kelvin.
        d_t (float, optional) : Shift for numerical derivative calculation.

    Returns:
        float or numpy.array : The constant volume heat capacity for a given
        partition functions at the given temperature(s) scaled appropriately.
    """
    return (
        (thermodynamic_energy(partition, temperature + d_t, scale_factor) -
         thermodynamic_energy(partition, temperature - d_t, scale_factor))
        / (2 * d_t))


# In Joules per Kelvin
def constant_pressure_heat_capacity(partition, temperature,
                                    scale_factor=const.N_A, *, d_t=1E-4):
    """
    Calculates Constant-pressure Heat capacity of a system for a
    given partition function at given temperature value(s).
    Default units are Joules *per mol* per Kelvin, since the default
    scaling is the Avogadro's number.
    Use 'scale_factor' to rescale (the Joules per Kelvin value) if needed.

    Args:
        partition (callable) : Partition function.
        temperature (float or numpy.array) : Temperature(s).
        scale_factor (float, optional) : Scaling of the energy
                                         (in Joules per Kelvin).
        The default is Avogadro's number for Joules per mol per Kelvin.
        d_t (float, optional) : Shift for numerical derivative calculation.

    Returns:
        float or numpy.array : The constant-pressure heat capacity a given
        partition functions at the given temperature(s) scaled appropriately.
    """
    return (enthalpy(partition, temperature + d_t, scale_factor) -
            enthalpy(partition, temperature - d_t, scale_factor)) / (2 * d_t)


############################################################################
# What follows is a wrapper for simpler use when one does not care about
#   specific components (e.g. translational, rotational, etc.) of a given
#   partition function.
############################################################################

class Thermodynamics:
    """
    A wrapper of the thermodynamic functions in the module, designed for
    simpler use when one does not care about specific components
    (e.g. translational, rotational, etc.) of a given partition function.

    After creating the object one can call directly:
        thermo_object.helmholtz_free_energy(t),
        thermo_object.entropy(t), etc.,
    without having to pass a particular partition function callable.
    Values are calculated based on the default (total) partition function.
    """

    def __init__(self, partition_function, pressure=101350):
        """
        Constructor.

        Args:
            partition_function (PartitionFunctionBase): the partition function.
            pressure (float, optional) : pressure for thermodynamic calculations
                                         (in Pa)

        Raises:
            ValueError: If the passed partition_function is not of type
                        PartitionFunctionBase
        """
        if not isinstance(partition_function, PartitionFunctionBase):
            raise ValueError(
                'PartitionFunctionBase class expected!')
        self.partition_function = partition_function
        self.set_pressure(pressure)

    def set_pressure(self, pressure):
        """
        Updates the internal callables, to calculate thermodynamic properties
        of the system at the new given pressure.

        Args:
            pressure (float): Pressure in Pa

        Raises:
            ValueError: Only implemented for diatomic molecules
        """
        self._callable = self.partition_function.get_default_callable(
            pressure=pressure)

        self.helmholtz_free_energy = partial(
            helmholtz_free_energy, self._callable, scale_factor=const.N_A)

        self.thermodynamic_energy = partial(
            thermodynamic_energy, self._callable, scale_factor=const.N_A)

        self.entropy = partial(entropy, self._callable,
                               scale_factor=const.N_A)

        self.enthalpy = partial(enthalpy, self._callable,
                                scale_factor=const.N_A)

        self.gibbs_free_energy = partial(
            gibbs_free_energy, self._callable, scale_factor=const.N_A)

        self.constant_volume_heat_capacity = partial(
            constant_volume_heat_capacity, self._callable,
            scale_factor=const.N_A)

        self.constant_pressure_heat_capacity = partial(
            constant_pressure_heat_capacity, self._callable,
            scale_factor=const.N_A)
