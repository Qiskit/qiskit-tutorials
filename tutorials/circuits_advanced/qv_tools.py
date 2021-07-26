import matplotlib.pyplot as plt
import numpy as np

from qiskit.quantum_info import Statevector

# a custom passmanager that does the compilation of QV circuits
def qv_passmanager(basis_gates, coupling_map, qubit_subset, backend_props,
                   instruction_durations, synthesis_fidelity, pulse_optimize):
    
    def _repeat_condition(property_set):
        return not property_set['depth_fixed_point']
    
    sub_coupling_map = coupling_map.reduce(qubit_subset)
    qr = QuantumRegister(size=len(qubit_subset), name='q')
    layout = Layout.from_intlist(sorted(qubit_subset), qr)

    _map = [BIPMapping(sub_coupling_map, objective='depth', time_limit=100)]

    _embed = [SetLayout(layout),
              FullAncillaAllocation(coupling_map),
              EnlargeWithAncilla(),
              ApplyLayout()]

    _check_depth = [Depth(),
                    FixedPoint('depth')]

    _optimize = [
        Collect2qBlocks(),
        ConsolidateBlocks(basis_gates=basis_gates),
        UnitarySynthesis(basis_gates, synthesis_fidelity, coupling_map, backend_props,
                         pulse_optimize=True, natural_direction=True),
        Optimize1qGatesDecomposition(basis_gates)
    ]

    _schedule = [
        ALAPSchedule(instruction_durations),
        DynamicalDecoupling(instruction_durations, dd_sequence=[XGate(), XGate()])
    ]

    pm = PassManager()
    pm.append(_map)                        # map to a subset of qubits, by choosing layout and inserting swaps
    pm.append(_embed)                      # embed the mapped circuit onto the larger device coupling map
    pm.append(_check_depth + _optimize,
              do_while=_repeat_condition)  # translate to & optimize over hardware native gates
    pm.append(_schedule)                   # dynamical decoupling on an as-late-as-possible schedule
    return pm


# plot a histogram of number of qubits and duration across all model circuits
def plot_resources(model_circuits_compiled, dt):
    fig, ax = plt.subplots(1, 3, figsize=(20,4))
    display_metrics = {'cx': [c.count_ops().get('cx', 0) for c in model_circuits_compiled],
                       'sx': [c.count_ops().get('sx', 0) for c in model_circuits_compiled],
                       'duration': [int(c.duration * dt * 1e9) for c in model_circuits_compiled]}

    for i, metric in enumerate(display_metrics):
        ax[i].set_title(
            f"{metric}\n"  \
            f"mean: {np.around(np.mean(display_metrics[metric]), 1)}    "  \
            f"median: {np.median(display_metrics[metric])}\n"  \
            f"min: {np.min(display_metrics[metric])}     " \
            f"max: {np.max(display_metrics[metric])}"
        )

        ax[i].hist(x=display_metrics[metric], 
                   range=(np.min(display_metrics[metric]), 
                          np.max(display_metrics[metric])))
    return ax


# functions for computing HOP
def get_ideal_probabilities(model_circuit):
    zero = Statevector.from_label('0' * model_circuit.num_qubits)
    sv = zero.evolve(model_circuit)
    return sv.probabilities_dict()
    

def get_heavy_strings(ideal_probs):
    prob_median = float(np.real(np.median(list(ideal_probs.values()))))
    heavy_strings = list(
        filter(
            lambda x: ideal_probs[x] > prob_median,
            list(ideal_probs.keys()),
        )
    )
    return prob_median, heavy_strings


def hop(counts, ideal_probs):
    _, heavy_strings = get_heavy_strings(ideal_probs)
    shots = sum(counts.values())
    heavy_output_probability = sum([counts.get(value, 0) for value in heavy_strings]) / shots
    return heavy_output_probability


# plot resulting HOPs and see if QV confidence is reached
def plot_hop_accumulative(hops):
    ntrials = len(hops)
    trials = np.arange(ntrials)

    hop_accumulative = np.cumsum(hops) / np.arange(1, ntrials + 1)
    two_sigma = 2 * (hop_accumulative * (1 - hop_accumulative) /
                     np.arange(1, ntrials + 1)) ** 0.5

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    # plot two-sigma shaded area
    ax.errorbar(trials, hop_accumulative, fmt="none", yerr=two_sigma, ecolor='lightgray',
                elinewidth=20, capsize=0, alpha=0.5, label='2$\\sigma$')
    # plot accumulative HOP
    ax.plot(trials, hop_accumulative, color='r', label='Cumulative HOP')
    # plot inidivual HOP as scatter
    ax.scatter(trials, hops, s=3, zorder=3, label='Individual HOP')
    # plot 2/3 success threshold
    ax.axhline(2/3, color='k', linestyle='dashed', linewidth=1, label='Threshold')

    ax.set_xlim(0, ntrials)
    ax.set_ylim(hop_accumulative[-1]-4*two_sigma[-1], hop_accumulative[-1]+4*two_sigma[-1])

    ax.set_ylim(.1, 1.)
    ax.set_xlabel('Number of Trials', fontsize=14)
    ax.set_ylabel('Heavy Output Probability', fontsize=14)

    # re-arrange legend order
    handles, labels = ax.get_legend_handles_labels()
    handles = [handles[1], handles[2], handles[0], handles[3]]
    labels = [labels[1], labels[2], labels[0], labels[3]]
    ax.legend(handles, labels)

    return ax