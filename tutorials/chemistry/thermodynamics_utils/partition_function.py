# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019, 2020
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""
This module implements defines a -- currently extremely sparse, since the
design is in flux -- partition function interface and implements a 1D (Diatomic)
partition function.
"""
import warnings
from inspect import signature
from abc import ABC, abstractmethod

import numpy as np
import qiskit.chemistry.constants as const


class PartitionFunctionBase(ABC):
    """
    Base class for a partition function object.
    Since design is not set in stone, only required method is a
    getDefaultCallable() method that returns a default (total) partition
    function callable object.
    """

    def __init__(self, molecule, energy_surface, vibronic_struct):
        """
        Constructor.

        Args:
            molecule: The underlying molecule (class Molecule)
            energy_surface: the potential energy surface used to provide
                        information on the molecule's equilibrium geometry and
                        ground state energy (class EnergySurfaceBase).
            vibronic_struct: the vibronic structure of the molecule providing
                        vibrational modes and energy levels
                        (class VibronicStructureBase).
        """

    @abstractmethod
    def get_default_callable(self, pressure=None):
        """ Get a default partition function callable """

    @abstractmethod
    def get_partition(self, *, part="total",
                      pressure=None, geometry=None):
        """
        Gets a callable to a partition function.

        Args:
            part (string): "total", "translational", "vibrational",
                           "rotational", "nuclear", "electronic"
                           (case insensitive and only compared to
                            the first three characters)
            pressure (float): Pressure (Pa).
            geometry (float, tuple): molecular geometry (specified
                            via the degrees of freedom for the molecule).
        """


class DifferentiableFunction:
    """
        A wrapper for a differentiable function to facilitate
        thermodynamic calculations.

        Given a callable function with numerical output, constructs a
        callable object with the same signature.

        The derivative (in the 'argument_name' variable) is also callable
        from the object(.D), as it is either provided analytically on
        construction or calculated numerically with central finite
        differences approximation.
    """

    def __init__(self, function, derivative=None, argument_name='t', fd=1E-4):
        """
        Constructor.
        Initializes the object with the given function (and its derivative)

        Args:
            function: the function callable.
            derivative: callable, optional
                        Callable object for the derivative. Default is None.
                        If provided, the other optional arguments are
                        disregarded and this is used for the objects .D
                        method.
            argument_name: string, optional
                        Argument with respect to which a numerical
                        derivative is calculated.
            fd: float, optional
                Finite difference for the numerical derivative calculation.

        Raises:
            ValueError: if function/derivative is not callable.
        """
        if not callable(function):
            raise ValueError("Provided function must be callable!")
        self.function = function
        if derivative is not None:
            if not callable(derivative):
                raise ValueError(
                    "Provided derivative must be callable"
                    " (and of the same signature)!")
            self.D = derivative
        else:
            self.argumentName = argument_name
            self.fd = fd
            self.D = self._derivative

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def _derivative(self, *args, **kwargs):
        sig = signature(self.function)
        ba = sig.bind(*args, **kwargs)
        arg_val = ba.arguments[self.argumentName]
        ba.arguments[self.argumentName] = arg_val + self.fd
        right_val = self.function(*ba.args, **ba.kwargs)
        ba.arguments[self.argumentName] = arg_val - self.fd
        left_val = self.function(*ba.args, **ba.kwargs)
        return (right_val - left_val) / (2 * self.fd)


class DiatomicPartitionFunction(PartitionFunctionBase):
    """
    Class implementing partition function for a diatomic molecule.
    Certain methods generalizable to bigger molecules may be moved to
    the PartitionFunctionBase class in the future.

    For the particular formulas implemented here, see the book
    'Statistical Mechanics' by Donald A. McQuarrie, isbn={9781891389153}

    """

    def __init__(self, molecule, energy_surface, vibronic_structure):
        """
        Constructor.
        Initializes the partition function with a molecule (Molecule), a
        potential energy surface (EnergySurfaceBase) and a molecular vibronic
        structure (VibronicStructureBase).

        Args:
            molecule: the underlying molecule.
            energy_surface (EnergySurfaceBase): 1D potential energy surface
            vibronic_structure (VibronicStructureBase): the molecular
                    vibronic structure
        """
        self.molecule = molecule
        self.energy_surface = energy_surface
        self.vibronic_structure = vibronic_structure

    def get_default_callable(self, pressure=None):
        """
        Returns a callable for the total partition function
                at the given pressure.
        """
        if len(self.molecule.masses) != 2:
            raise ValueError(
                'Only implemented for diatomic molecules!')
        is_homonuclear = (self.molecule.masses[0] == self.molecule.masses[1])
        if is_homonuclear:
            return self.get_partition(split='eq', pressure=pressure)
        else:
            return self.get_partition(pressure=pressure)

    def get_partition(self, *, part="total", split=None,
                      pressure=None, geometry=None):
        """
        The main method for accessing specific components of the partition
        function.

        Returns a callable (as a DifferentialFunction, so it has
            derivative information) for the specified component partition
            function (total, translational, vibrational etc.) at a
            given pressure and molecule geometry (usually equilibrium).

            In addition, one can get a specific split for a homonuclear
            (e.g. H2, D2) molecule "equilibrium"/"ortho"/"para"/"mixture".

        Args:
            part: optional, string,
                The component of the partition function "tot(al)",
                "trans(lational)", "vib(rational)", "rot(atinal)", etc.
            split: optional, string,
                Further specification for the split of the
                rotational partition function in the homonuclear case.
                (See McQuarrie 6-40,41... p. 102 - 107)
            pressure: optional, float,
                Specified pressure for the system (used in the
                translational part). Default is 1 atmosphere (in Pa)
            geometry: optional, float,
                Internuclear distance for the molecular geometry.
                Default is the equilibrium distance (corresponding to minimal
                molecular energy).

        Raises:
            ValueError: if part is not recognized.
        """
        p = pressure if pressure is not None else 101325
        r = (geometry if geometry is not None else
             self.energy_surface.get_equilibrium_geometry(1E-10))  # meters

        __trans = DifferentiableFunction(
            lambda t: self.eval_translational(p, t),
            # lambda t: self.eval_d_dt_translational(p,t))
            lambda t: self.eval_d_dt_translational_volume_corrected(p, t))

        __vib = DifferentiableFunction(
            lambda t: self.eval_vibrational(t),
            lambda t: self.eval_d_dt_vibrational(t))

        __rot = DifferentiableFunction(
            lambda t: self.eval_rotational(r, t),
            lambda t: self.eval_d_dt_rotational(r, t))

        if split is not None:
            if not (part.lower().startswith('rot')
                    or part.lower().startswith('tot')):
                warnings.warn(
                    "Split in para/ortho/mix parts only makes"
                    " sense for Rotational/Total partitions.",
                    RuntimeWarning)
            if split.lower().startswith('eq'):
                __rot = DifferentiableFunction(
                    lambda t: self.eval_rotational(r, t, True)[0],
                    lambda t: self.eval_d_dt_rotational(r, t, True)[0])
            if split.lower().startswith('para'):
                __rot = DifferentiableFunction(
                    lambda t: self.eval_rotational(r, t, True)[1],
                    lambda t: self.eval_d_dt_rotational(r, t, True)[1])
            if split.lower().startswith('ortho'):
                __rot = DifferentiableFunction(
                    lambda t: self.eval_rotational(r, t, True)[2],
                    lambda t: self.eval_d_dt_rotational(r, t, True)[2])
            if split.lower().startswith('mix'):
                __rot = DifferentiableFunction(
                    lambda t: self.eval_rotational(r, t, True)[3],
                    lambda t: self.eval_d_dt_rotational(r, t, True)[3])

        # __nuc = DifferentiableFunction(
        #     lambda t: self.eval_nuclear(self, t),
        #     lambda t: self.eval_d_dt_nuclear(self, t))

        # __ele = DifferentiableFunction(
        #     lambda t: self.eval_nuclear(self, t),
        #     lambda t: self.eval_d_dt_nuclear(self, t))

        __tot = DifferentiableFunction(
            lambda t: __trans(t) * __vib(t) * __rot(t),
            lambda t: (__trans.D(t) * __vib(t) * __rot(t) +
                       __trans(t) * __vib.D(t) * __rot(t) +
                       __trans(t) * __vib(t) * __rot.D(t)
                       )
        )

        if part.lower().startswith('trans'):
            return __trans
        if part.lower().startswith('vib'):
            return __vib
        if part.lower().startswith('rot'):
            return __rot
        # if partStr.lower().startswith('nuc'):
        #     return self.__nuc
        # if partStr.lower().startswith('ele'):
        #     return self.__ele
        if part.lower().startswith('tot'):
            return __tot

        # If we're here - the 'part' string is invalid
        raise ValueError('Unrecognized partition "{}"'.format(part))
        # return self.getDefaultCallable(pressure)

    # ******************** Translational part ********************

    def eval_translational(self, p, t):
        """
        Translational component of the molecular partition function.

        Arguments:
            p: pressure in Pa
            t: temperature in K

        Uses internal:
            m: mass of molecule in kg

        Returns:
            Value of translational partition function
        """
        m = sum(self.molecule.masses)

        debrog = (
            (const.H_J_S ** 2 / (2 * np.pi * m * const.KB_J_PER_K * t))
            ** (1 / 2)
        )
        v = (const.KB_J_PER_K * t) / p
        q_trans = v / debrog ** 3

        return q_trans

    def eval_d_dt_translational(self, p, t):
        """ We should not be using that - use the volume corrected one"""
        raise NotImplementedError

    def eval_d_dt_translational_fd(self, p, t):
        """ Finite Difference derivative w.r.t. t of the translational part"""
        diff = 1e-6
        return (self.eval_translational(p, t + diff) -
                self.eval_translational(p, t)) / diff

    def eval_d_dt_translational_volume_corrected(self, p, t):
        """
        Derivative w.r.t. t, WHEN VOLUME IS HELD CONSTANT
        Note that this is not the "mathematical" t-derivative of
        eval_translation, but is nevertheless what is used for
        further thermodynamic calculations!
        """

        return 3 / (2 * t) * self.eval_translational(p, t)

    # ******************** Vibrational part ********************

    def _eval_vibrational(self, t, evaluate_gradient=False):
        """
        Vibrational component of the molecular partition function.

        If evaluate_gradient=True, calculates the t-derivative instead.

        Arguments:
            t: temperature in K
            evaluate_gradient: True if derivative is

        Returns:
            Value of the vibrational partition function or its derivative.

        """
        beta = 1 / (const.KB_J_PER_K * t)
        dbdt = -1 / (const.KB_J_PER_K * t * t)

        nv = 0
        q_vib_ah = 0

        nmax = self.vibronic_structure.get_maximum_trusted_level()

        # if nmax > 100:
        #     print(
        #         "Warning, limiting vibrational partition"
        #         " function summation to 100 terms!")
        #     nmax = 100

        while nv <= nmax:
            e_n = self.vibronic_structure.vibrational_energy_level(
                nv) * const.HARTREE_TO_J
            q_vib_ah += (np.exp(-beta * e_n) if not evaluate_gradient
                         else (-dbdt * e_n) * np.exp(-beta * e_n))
            nv += 1

        return q_vib_ah

    def eval_vibrational(self, t):
        """
        Vibrational component of the molecular partition function.

        Arguments:
            t: temperature in K

        Returns:
            Value of the vibrational partition function.

        """
        return self._eval_vibrational(t)

    def eval_d_dt_vibrational(self, t):
        """
        Derivative of the vibrational component of the molecular
        partition function.

        Arguments:
            t: temperature in K

        Returns:
            Value of the vibrational partition function derivative.

        """
        return self._eval_vibrational(t, evaluate_gradient=True)

    def eval_d_dt_vibrational_fd(self, t):
        """ Finite Difference derivative w.r.t. t of the vibrational part"""
        diff = 1e-6
        return (self.eval_vibrational(t + diff) -
                self.eval_vibrational(t)) / diff

    # *************** Rotational part (high-temperature limit) ***************

    def _eval_rotational_high_temp(self, r0, t, evaluate_gradient=False):
        """
        Rotational molecular partition function in the
        high temperature limit.
        Valid only when theta_r << t
        See McQuarrie 6-47

        Arguments:
            r0: bond length
            t: temperature in K
            evaluate_gradient: if True evaluates the t-derivative instead.

        Uses internal:
            m_a: mass of atom A in molecule in kg
            m_b: mass of atom B in molecule in kg

        Returns:
            Value of the rotational partition function or its derivative.
        """

        m_a = self.molecule.masses[0]
        m_b = self.molecule.masses[1]

        # TODO: Compare names instead?
        # now we need to determine the symmetry number
        if m_a == m_b:
            sigma = 2  # if the masses are the same, symmetry number is 2
        else:
            sigma = 1

        m_r = (m_a * m_b) / (m_a + m_b)  # reduced mass

        # TODO: Can/Should we take this directly from molecule?
        intertia = m_r * (r0 ** 2)  # moment of inertia
        # rotational temp (K)
        theta_r = const.HBAR_J_S ** 2 / (2 * intertia * const.KB_J_PER_K)

        q_rot_ht_limit = (t / (sigma * theta_r)) * (
            1
            + theta_r / (3 * t)
            + (1 / 15) * (theta_r / t) ** 2
            + (4 / 315) * (theta_r / t) ** 3
        )

        d_dt_q_rot_ht_limit = (
            1 / (sigma * theta_r)
            - (1 / 15) * (theta_r / sigma) * (1 / t) ** 2
            - (8 / 315) * (theta_r ** 2 / sigma) * (1 / t) ** 3
        )

        return (q_rot_ht_limit if not evaluate_gradient
                else d_dt_q_rot_ht_limit)

    def eval_rotational_high_temp(self, r0, t):
        """
        Rotational molecular partition function in the high temperature limit.
        Valid only when theta_r << t; See McQuarrie 6-47

        Arguments:
            r0: bond length
            t: temperature in K

        Returns:
            Value of the rotational partition function.
        """
        return self._eval_rotational_high_temp(r0, t)

    def eval_d_dt_rotational_high_temperature(self, r0, t):
        """
        Derivative (w.r.t. temperature) of the rotational molecular
        partition function in the high temperature limit.
        Valid only when theta_r << t; See McQuarrie 6-47

        Arguments:
            r0: bond length
            t: temperature in K

        Returns:
            Value of the rotational partition function derivative.
        """
        return self._eval_rotational_high_temp(r0, t, True)

    def eval_d_dt_rotational_high_temperature_fd(self, r0, t):
        """
        Finite Difference derivative w.r.t. t
        of the high temp limit rotational partition function
        """
        diff = 1e-6
        return (self.eval_rotational_high_temp(r0, t + diff) -
                self.eval_rotational_high_temp(r0, t)) / diff

    # *************** Rotational part (general derivation) ***************

    def _eval_rotational(self, r, t, split_para_ortho=False,
                         evaluate_gradient=False):
        """
        Rotational molecular partition function
        See McQuarrie 6-40,41... p. 102 - 107
        Here, the equilibrium concentration of o-H2 and p-H2 is computed
        at temperature, this is used to compute q_rot.

        Arguments:
            r: bond length
            t: temperature in K
            split_para_ortho: if True returns the para- and ortho- components
                separately.
            evaluate_gradient: if True, calculates derivative(s) with respect
                to the temperature instead

        Returns
            Single (equilibrium) value if split_para_ortho is False,
            "equilibrium", "para", "ortho" and "mix" values if True
            (or corresponding derivative value(s))
        """
        m_a = self.molecule.masses[0]
        m_b = self.molecule.masses[1]
        m_r = (m_a * m_b) / (m_a + m_b)  # reduced mass

        intertia = m_r * (r ** 2)  # moment of inertia
        # rotational temp (K)
        theta_r = const.HBAR_J_S ** 2 / (2 * intertia * const.KB_J_PER_K)
        b_bar = theta_r * const.KB_J_PER_K  # rot constant (j/molecule)

        # d_e = self.potential.dissociation_energy(const.HARTREE_TO_J)

        j = 0

        q_rot_evn = 0
        q_rot_odd = 0
        d_q_rot_evn = 0
        d_q_rot_odd = 0
        e_rot = 0
        # while e_rot < d_e:
        while j < 1000:
            if j % 2 == 0:
                # value
                q_rot_evn += (2 * j + 1) * np.exp(
                    (-theta_r * j * (j + 1)) / t
                )
                # derivative d_dT
                d_q_rot_evn += ((2 * j + 1) *
                                np.exp((-theta_r * j * (j + 1)) / t)
                                * (theta_r * j * (j + 1)) / t ** 2
                                )
            else:
                # value
                q_rot_odd += (2 * j + 1) * np.exp(
                    (-theta_r * j * (j + 1)) / t
                )
                # derivative d_dT
                d_q_rot_odd += ((2 * j + 1) *
                                np.exp((-theta_r * j * (j + 1)) / t)
                                * (theta_r * j * (j + 1)) / t ** 2
                                )
            j += 1
            e_rot = b_bar * j * (j + 1)

        if not split_para_ortho:
            return (q_rot_evn + q_rot_odd if not evaluate_gradient
                    else d_q_rot_evn + d_q_rot_odd)
        else:
            spin = self.molecule.spins[0]
            if (m_a != m_b) or (spin != self.molecule.spins[1]):
                raise ValueError("Ortho/Para split only allowed"
                                 " for identical atoms.")
            ortho = q_rot_evn if (spin == 1) else q_rot_odd
            d_ortho = d_q_rot_evn if (spin == 1) else d_q_rot_odd
            para = q_rot_odd if (spin == 1) else q_rot_evn
            d_para = d_q_rot_odd if (spin == 1) else d_q_rot_evn
            q_rot_ortho = (spin + 1) * (2 * spin + 1) * ortho
            d_q_rot_ortho = (spin + 1) * (2 * spin + 1) * d_ortho
            q_rot_para = spin * (2 * spin + 1) * para
            d_q_rot_para = spin * (2 * spin + 1) * d_para
            q_rot_eq = q_rot_para + q_rot_ortho
            d_q_rot_eq = d_q_rot_para + d_q_rot_ortho
            frac_para = q_rot_para / (q_rot_para + q_rot_ortho)
            q_rot_mix = (para ** frac_para) * (ortho ** (1 - frac_para))
            d_q_rot_mix = (
                self._d_dx_expr(
                    para, spin * (2 * spin + 1),
                    ortho, (spin + 1) * (2 * spin + 1)) * d_para +
                self._d_dx_expr(
                    ortho, (spin + 1) * (2 * spin + 1),
                    para, spin * (2 * spin + 1)) * d_ortho
            )
            if evaluate_gradient:
                return np.array([d_q_rot_eq, d_q_rot_para,
                                 d_q_rot_ortho, d_q_rot_mix])
            return np.array([q_rot_eq, q_rot_para, q_rot_ortho, q_rot_mix])

    def eval_rotational(self, r, t, split_para_ortho=False):
        """
        Rotational molecular partition function
        See McQuarrie 6-40,41... p. 102 - 107
        Here, the equilibrium concentration of o-H2 and p-H2 is computed
        at temperature, this is used to compute the rotational partition
        function.

        Arguments:
            r: bond length
            t: temperature in K
            split_para_ortho: if True returns the para- and ortho- components
                separately.

        Returns
            Single (equilibrium) value if split_para_ortho is False,
            "equilibrium", "para", "ortho" and "mix" values if True
            (or corresponding derivative value(s))
        """
        return self._eval_rotational(
            r, t, split_para_ortho, evaluate_gradient=False)

    def eval_d_dt_rotational(self, r, t, split_para_ortho=False):
        """
        Derivative (w.r.t. temperature) of the rotational molecular
        partition function.
        See McQuarrie 6-40,41... p. 102 - 107
        Here, the equilibrium concentration of o-H2 and p-H2 is computed
        at temperature, this is used to compute the rotational partition
        function.

        Arguments:
            r: bond length
            t: temperature in K
            split_para_ortho: if True returns the para- and ortho- components
                separately.

        Returns
            Single (equilibrium) value if split_para_ortho is False,
            "equilibrium", "para", "ortho" and "mix" values if True
        """
        return self._eval_rotational(
            r, t, split_para_ortho, evaluate_gradient=True)

    def eval_d_dt_rotational_fd(self, r, t, split_para_ortho=False):
        """ Finite Difference derivative w.r.t. t of the rotational part"""
        diff = 1e-6
        return (self.eval_rotational(r, t + diff, split_para_ortho) -
                self.eval_rotational(r, t, split_para_ortho)) / diff

    # ************ Nuclear part (low-temperature approximation) ************

    def eval_nuclear(self, p, t):
        """ Nuclear partition function currently approximated as 1.0 """
        return 1.0

    def eval_d_dt_nuclear(self, p, t):
        """ Nuclear partition function currently approximated as 1.0 """
        return 0.0

    # ***************** Electronic part (approximation) *****************

    def eval_electronic(self, p, t):
        """ Electronic partition function currently approximated as 1.0 """
        return 1.0

    def eval_d_dt_electronic(self, p, t):
        """ Electronic partition function currently approximated as 1.0 """
        return 0.0

    # ***************** Electronic part (approximation) *****************

    @staticmethod
    def _d_dx_expr(x, c, y, d):
        """
        x-partial derivative of x ** (c*x/(c*x+d*y)) * y ** (d*y/(c*x+d*y))
        used in (the analytical derivative of) the
        equilibrium ortho-para mixture
        """
        return (
            -c * d * x ** (c * x / (c * x + d * y))
            * y * y ** (d * y / (c * x + d * y))
            * np.log(y) / (c * x + d * y) ** 2
            +
            x ** (c * x / (c * x + d * y)) *
            y ** (d * y / (c * x + d * y)) *
            (c / (c * x + d * y) +
             (-c ** 2 * x / (c * x + d * y)
              ** 2 + c / (c * x + d * y)) * np.log(x))
        )
