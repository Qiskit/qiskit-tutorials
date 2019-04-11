# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=invalid-name,anomalous-backslash-in-string,ungrouped-imports, import-error

"""Plotting Wigner functions."""

import numpy as np
from qiskit.tools.visualization._matplotlib import HAS_MATPLOTLIB

if HAS_MATPLOTLIB:
    from matplotlib import cm
    from matplotlib import pyplot as plt


def plot_wigner_function(state, res=100, figsize=None):
    """Plot the equal angle slice spin Wigner function of an arbitrary
    quantum state.

    Args:
        state (np.matrix[[complex]]):
            - Matrix of 2**n x 2**n complex numbers
            - State Vector of 2**n x 1 complex numbers
        res (int) : number of theta and phi values in meshgrid
            on sphere (creates a res x res grid of points)
        figsize (tuple): Figure size in inches.
    Returns:
         matplotlib.Figure: The matplotlib.Figure of the visualization
    Raises:
        ImportError: Requires matplotlib.

    References:
        [1] T. Tilma, M. J. Everitt, J. H. Samson, W. J. Munro,
        and K. Nemoto, Phys. Rev. Lett. 117, 180401 (2016).
        [2] R. P. Rundle, P. W. Mills, T. Tilma, J. H. Samson, and
        M. J. Everitt, Phys. Rev. A 96, 022117 (2017).
    """
    if not HAS_MATPLOTLIB:
        raise ImportError('Must have Matplotlib installed.')
    if figsize is None:
        figsize = (11, 9)

    state = np.asarray(state)
    if state.ndim == 1:
        state = np.outer(state,
                         state)  # turns state vector to a density matrix
    num = int(np.log2(state.shape[0]))  # number of qubits
    phi_vals = np.linspace(0, np.pi, num=res,
                           dtype=np.complex_)
    theta_vals = np.linspace(0, 0.5*np.pi, num=res,
                             dtype=np.complex_)  # phi and theta values for WF
    w = np.empty([res, res])
    harr = np.sqrt(3)
    delta_su2 = np.zeros((2, 2), dtype=np.complex_)

    # create the spin Wigner function
    for theta in range(res):
        costheta = harr*np.cos(2*theta_vals[theta])
        sintheta = harr*np.sin(2*theta_vals[theta])

        for phi in range(res):
            delta_su2[0, 0] = 0.5*(1+costheta)
            delta_su2[0, 1] = -0.5*(np.exp(2j*phi_vals[phi])*sintheta)
            delta_su2[1, 0] = -0.5*(np.exp(-2j*phi_vals[phi])*sintheta)
            delta_su2[1, 1] = 0.5*(1-costheta)
            kernel = 1
            for _ in range(num):
                kernel = np.kron(kernel,
                                 delta_su2)  # creates phase point kernel

            w[phi, theta] = np.real(np.trace(state.dot(kernel)))  # Wigner function

    # Plot a sphere (x,y,z) with Wigner function facecolor data stored in Wc
    fig = plt.figure(figsize=figsize)
    ax = fig.gca(projection='3d')
    w_max = np.amax(w)
    # Color data for plotting
    w_c = cm.RdBu((w+w_max)/(2*w_max))  # color data for sphere
    w_c2 = cm.RdBu((w[0:res, int(res/2):res]+w_max)/(2*w_max))  # bottom
    w_c3 = cm.RdBu((w[int(res/4):int(3*res/4), 0:res]+w_max) /
                   (2*w_max))  # side
    w_c4 = cm.RdBu((w[int(res/2):res, 0:res]+w_max)/(2*w_max))  # back

    u = np.linspace(0, 2 * np.pi, res)
    v = np.linspace(0, np.pi, res)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))  # creates a sphere mesh

    ax.plot_surface(x, y, z, facecolors=w_c,
                    vmin=-w_max, vmax=w_max,
                    rcount=res, ccount=res,
                    linewidth=0, zorder=0.5,
                    antialiased=False)  # plots Wigner Bloch sphere

    ax.plot_surface(x[0:res, int(res/2):res],
                    y[0:res, int(res/2):res],
                    -1.5*np.ones((res, int(res/2))),
                    facecolors=w_c2,
                    vmin=-w_max, vmax=w_max,
                    rcount=res/2, ccount=res/2,
                    linewidth=0, zorder=0.5,
                    antialiased=False)  # plots bottom reflection

    ax.plot_surface(-1.5*np.ones((int(res/2), res)),
                    y[int(res/4):int(3*res/4), 0:res],
                    z[int(res/4):int(3*res/4), 0:res],
                    facecolors=w_c3,
                    vmin=-w_max, vmax=w_max,
                    rcount=res/2, ccount=res/2,
                    linewidth=0, zorder=0.5,
                    antialiased=False)  # plots side reflection

    ax.plot_surface(x[int(res/2):res, 0:res],
                    1.5*np.ones((int(res/2), res)),
                    z[int(res/2):res, 0:res],
                    facecolors=w_c4,
                    vmin=-w_max, vmax=w_max,
                    rcount=res/2, ccount=res/2,
                    linewidth=0, zorder=0.5,
                    antialiased=False)  # plots back reflection

    ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    ax.set_zticks([], [])
    ax.grid(False)
    ax.xaxis.pane.set_edgecolor('k')
    ax.yaxis.pane.set_edgecolor('k')
    ax.zaxis.pane.set_edgecolor('k')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    m = cm.ScalarMappable(cmap=cm.RdBu)
    m.set_array([-w_max, w_max])
    cbar = plt.colorbar(m, shrink=0.5, aspect=10,
                        ticks=[-1, -0.5, 0, 0.5, 1.0])
    cbar.ax.tick_params(labelsize=14)
    plt.close(fig)
    return fig


def plot_wigner_curve(wigner_data, xaxis=None, filename=None):
    """Plots a curve for points in phase space of the spin Wigner function.

    Args:
        wigner_data(np.array): an array of points to plot as a 2d curve
        xaxis (np.array):  the range of the x axis
        filename (str): the output file to save the plot as. If specified it
            will save and exit and not open up the plot in a new window.
    Raises:
        ImportError: Requires matplotlib.
    """
    if not HAS_MATPLOTLIB:
        raise ImportError('Must have Matplotlib installed.')
    if not xaxis:
        xaxis = np.linspace(0, len(wigner_data)-1, num=len(wigner_data))

    plt.plot(xaxis, wigner_data)
    if filename:
        plt.savefig(filename)
    else:
        plt.show()


def plot_wigner_plaquette(wigner_data, max_wigner='local', filename=None):
    """Plots plaquette of wigner function data, the plaquette will
    consist of circles each colored to match the value of the Wigner
    function at the given point in phase space.

    Args:
        wigner_data (matrix): array of Wigner function data where the
                            rows are plotted along the x axis and the
                            columns are plotted along the y axis
        max_wigner (str or float):
            - 'local' puts the maximum value to maximum of the points
            - 'unit' sets maximum to 1
            - float for a custom maximum.
        filename (str): the output file to save the plot as. If specified it
            will save and exit and not open up the plot in a new window.
    Raises:
        ImportError: Requires matplotlib.
    """
    if not HAS_MATPLOTLIB:
        raise ImportError('Must have Matplotlib installed.')
    wigner_data = np.matrix(wigner_data)
    dim = wigner_data.shape

    if max_wigner == 'local':
        w_max = np.amax(wigner_data)
    elif max_wigner == 'unit':
        w_max = 1
    else:
        w_max = max_wigner  # For a float input
    w_max = float(w_max)

    cmap = plt.cm.get_cmap('seismic_r')

    xax = dim[1]-0.5
    yax = dim[0]-0.5
    norm = np.amax(dim)

    fig = plt.figure(figsize=((xax+0.5)*6/norm, (yax+0.5)*6/norm))
    ax = fig.gca()

    for x in range(int(dim[1])):
        for y in range(int(dim[0])):
            circle = plt.Circle(
                (x, y), 0.49, color=cmap((wigner_data[y, x]+w_max)/(2*w_max)))
            ax.add_artist(circle)

    ax.set_xlim(-1, xax+0.5)
    ax.set_ylim(-1, yax+0.5)
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    m = cm.ScalarMappable(cmap=cm.seismic_r)
    m.set_array([-w_max, w_max])
    plt.colorbar(m, shrink=0.5, aspect=10)
    if filename:
        plt.savefig(filename)
    else:
        plt.show()


def plot_wigner_data(wigner_data, phis=None, method=None, filename=None):
    """Plots Wigner results in appropriate format.

    Args:
        wigner_data (numpy.array): Output returned from the wigner_data
            function
        phis (numpy.array): Values of phi
        method (str or None): how the data is to be plotted, methods are:
            point: a single point in phase space
            curve: a two dimensional curve
            plaquette: points plotted as circles
        filename (str): the output file to save the plot as. If specified it
            will save and exit and not open up the plot in a new window.
    Raises:
        ImportError: Requires matplotlib.
    """
    if not HAS_MATPLOTLIB:
        raise ImportError('Must have Matplotlib installed.')
    if not method:
        wig_dim = len(np.shape(wigner_data))
        if wig_dim == 1:
            if np.shape(wigner_data) == 1:
                method = 'point'
            else:
                method = 'curve'
        elif wig_dim == 2:
            method = 'plaquette'

    if method == 'curve':
        plot_wigner_curve(wigner_data, xaxis=phis, filename=filename)
    elif method == 'plaquette':
        plot_wigner_plaquette(wigner_data, filename=filename)
    elif method == 'state':
        plot_wigner_function(wigner_data)
    elif method == 'point':
        plot_wigner_plaquette(wigner_data, filename=filename)
        print('point in phase space is '+str(wigner_data))
    else:
        print("No method given")
