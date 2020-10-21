# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Utilities for Analytic Vibronic Structure Calculations for diatomic molecules
"""
import warnings

import numpy as np
from scipy.linalg import eigh_tridiagonal, eigvalsh_tridiagonal

import qiskit.chemistry.constants as const
from qiskit.chemistry.algorithms.pes_samplers.potentials.potential_base import VibronicStructureBase


class VibronicStructure1DFD(VibronicStructureBase):
    """
    A simple finite difference calculation of vibrational 
    energy levels of an arbitrary 1D potential energy surface.
    """

    def __init__(self, molecule, energy_surface, *,
                 num_intervals=10000):
        """
        Constructor.
        Initializes the class with a molecule (needed for mass) and an
        energy surface.
        Computes and stores the eigenvalues on construction.

        Args:
            molecule (Molecule): the underlying molecule.
            energy_surface (EnergySurfaceBase): the energy surface
            num_intervals (int): the number of intervals for discretization
        """
        self.molecule = molecule
        self.energy_surface = energy_surface
        self.num_intervals = num_intervals
        self.energy_levels = None
        self._mA = molecule.masses[0]
        self._mB = molecule.masses[1]

    def initialize(self):
        self.potential = self.get_centered_potential(self.energy_surface)
        self.left, self.right = self.find_bounds(self.potential)
        
        bounds = self.energy_surface.get_trust_region()
        bound_left = (bounds[0] -
                      self.energy_surface.get_equilibrium_geometry())
        bound_right = (bounds[1] -
                      self.energy_surface.get_equilibrium_geometry())
        self.left = max(self.left, bound_left)
        self.right = min(self.right, bound_right)
        if self.right - self.left < 1:
            warnings.warn(
                "Attempting to compute eigenvalues in a fairly small trusted"
                "region ({},{})".format(self.left, self.right),
                RuntimeWarning)
        
        self.energy_levels = self._solve()

    def _get_discrete_potential(self):
        """ Returns an array of potential energy surface values """
        n = self.num_intervals
        delta_x = (self.right - self.left) / n
        pot = np.zeros(n+1)
        for i in range(n+1):
            pot[i] = self.potential(self.left + i*delta_x)
        return pot

    def _solve(self, return_wave_function=False):
        """ Solves for the eigenvalues of the 1D Schroedinger equation """
        n = self.num_intervals
        delta_x = (self.right - self.left) / n
        d = 2.0/delta_x ** 2 * np.ones(n+1)
        e = -1.0/delta_x ** 2 * np.ones(n)

        _mA = self.molecule.masses[0]
        _mB = self.molecule.masses[1]
        reduced_mass = _mA*_mB/(_mA+_mB)
        scale = (const.J_TO_HARTREE * const.HBAR_J_S * const.M_TO_ANGSTROM *
                 const.M_TO_ANGSTROM * const.HBAR_J_S / (2*reduced_mass))

        d *= scale
        e *= scale
        d += self._get_discrete_potential()

        EIG_SOLVER = eigvalsh_tridiagonal
        if return_wave_function:
            EIG_SOLVER = eigh_tridiagonal

        return EIG_SOLVER(d, e)

    @staticmethod
    def get_centered_potential(pot):
        """ 
        Centers the potential so that the minimum value is 0 Hartrees,
        and is achieved at 0 Angstroms.
        """
        return lambda x: (pot.eval(x+pot.get_equilibrium_geometry()) -
                          pot.get_minimal_energy())

    @staticmethod
    def find_bounds(centered_pot, *,
                    max_val=500,
                    min_x=-10, max_x=10):
        """
        Finds discretization bounds for a cenetered potential
        (see get_centered_potential), i.e. an interval containing 0, with
        maximum length max_length, such that (for a generally smooth
        potential) the potential values inside it do not exceed the given
        max_val.
        """

        left = 0
        while centered_pot(left) < max_val and left > min_x:
            left -= 1

        right = 0
        while centered_pot(right) < max_val and right < max_x:
            right += 1

        return left, right

    # Implementing the VibronicStructureBase interface

    def get_num_modes(self):
        """ returns the number of vibrational modes for the molecule """
        return 1

    def vibrational_energy_level(self, n, mode=0):
        if mode > 0:
            raise ValueError('1D energy surfaces have a single mode')
        if self.energy_levels is None:
            self.initialize()

        return self.energy_levels[n]
