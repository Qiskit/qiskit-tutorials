import math
from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from qiskit.quantum_info import Statevector
from qiskit.circuit import QuantumCircuit, Delay

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


# removing delays prior to ideal simulation
def remove_delay(circ):
    new_circ = QuantumCircuit(*circ.qregs, *circ.cregs)
    new_circ.name = circ.name
    for op, qargs, cargs in circ.data:
        if not isinstance(op, Delay):
            new_circ.append(op, qargs, cargs)
    return new_circ


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
    print(hop_accumulative[-1] - two_sigma[-1])
    success = False
    if (hop_accumulative[-1] - two_sigma[-1]) > 2/3:
        success = True

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
    ax.set_title(
        f'mean hop: {hop_accumulative[-1]:.2f}\n'
        f'±2σ: [{(hop_accumulative[-1] - two_sigma[-1]):.3f}, {(hop_accumulative[-1] + two_sigma[-1]):.3f}]\n'
        f'success: {success}'
    )

    return ax


# tailoring orientation

def natural_cx_on_qubits(qubits, backend, durations=None):
    '''Build a natural coupling map by inferring natural gate
    direction based on gate durations. If durations is given it
    over-rides the backend-reported ones.'''
    cmap = deepcopy(backend.configuration().coupling_map)
    props = deepcopy(backend.properties())
    to_remove = []
    for l in cmap:
        if l[0] not in qubits or l[1] not in qubits:
            to_remove.append(l)
            continue
        reverse_l = l[::-1]
        if durations:
            cx_length = durations.duration_by_name_qubits.get(('cx', tuple(l)), math.inf)
            reverse_cx_length = durations.duration_by_name_qubits.get(('cx', tuple(reverse_l)), None)
            if reverse_cx_length and reverse_cx_length < cx_length:
                to_remove.append(l)
        else:    
            cx_length = props.gate_length('cx', l)
            reverse_cx_length = None
            if reverse_l in cmap:
                reverse_cx_length = props.gate_length('cx', reverse_l)
            if reverse_cx_length and reverse_cx_length < cx_length:
                to_remove.append(l)
    for l in to_remove:
        cmap.remove(l)

    return cmap

def get_qubit_durations(circs, qubits, backend):
    """Take a scheduled circuit and log durations per qubits."""
    dt = backend.configuration().dt
    qubit_durations = {q : [] for q in qubits}
    for circ in tqdm(circs):
        for qubit in qubits:
            qubit_duration = circ.qubit_duration(qubit)
            qubit_durations[qubit].append(qubit_duration * dt * 1e6)  # record in us
    return qubit_durations

def get_circuit_durations(circs, backend):
    """This records total circuit duration scheduled circuits."""
    dt = backend.configuration().dt
    circuit_durations = []
    for circ in circs:
        circuit_durations.append(circ.duration * dt * 1e6)
    return circuit_durations

def get_link_usage(circs, cmap, backend):
    """How many of each CNOT is used."""
    link_usage = {tuple(l) : [0] * len(circs) for l in cmap}
    for i, circ in tqdm(enumerate(circs)):
        for gate, qargs, cargs in circ.data:
            if gate.name == 'cx' or gate.name == 'ecr':
                link_usage[(qargs[0].index, qargs[1].index)][i] += 1
    return link_usage

def get_t1_t2(backend, qubits):
    qubit_t1 = {q : [] for q in qubits}
    qubit_t2 = {q : [] for q in qubits}
    for qubit in qubits:
        props = backend.properties()
        qubit_t1[qubit] = props.t1(qubit) * 1e6
        qubit_t2[qubit] = props.t2(qubit) * 1e6
    return qubit_t1, qubit_t2
    
def get_cx_errors(backend, cmap):
    link_fid = {tuple(link) : [] for link in cmap}
    for link in cmap:
        props = backend.properties()
        link_fid[tuple(link)] = (1-props.gate_error('cx', link))*100
    return link_fid

def cost_durations_t1t2s(ds, t1s, t2s):
    '''sum(duration / t1) over all qubits.
    lower is better.'''
    return sum([d/t2 for d, t1, t2 in zip(ds, t1s, t2s)])

def choose_best_for_duration(backend, t1s, t2s, candidate_durations):
    qubits = list(candidate_durations[0].keys())
    num_circs = len(candidate_durations[0][qubits[0]])

    qubit_durations_best = deepcopy(candidate_durations[0])

    for sample_circuit in range(num_circs):
        circuit_cost = math.inf
        for durations in candidate_durations:
            ds = [durations[q][sample_circuit] for q in qubits]
            cost = cost_durations_t1t2s(ds, t1s, t2s)
            if cost < circuit_cost:
                circuit_cost = cost
                for q in qubits:
                    qubit_durations_best[q][sample_circuit] = durations[q][sample_circuit]

    return qubit_durations_best

def plot_improvement_duration(backend, candidate_durations, sample_circuit=None, metric='average'):
    """Plot improvement due to picking a better layout orientation on a symmetrical topology.
    
    Args:
        backend (BaseBackend): a backend to get data (properties) from
        candidate_durations: candidate symmetries and durations associated with each (going to pick best)
        sample_circuit (int or None): show change for a particular circuit (None to omit)
        metric (str): 'average', 'median', 'max' or 'min'
    """
    metric_func = {
        'average': np.average,
        'median': np.median,
        'max': np.max,
        'min': np.min
    }

    qubits = list(candidate_durations[0].keys())
    qubit_t1, qubit_t2 = get_t1_t2(backend, qubits)
    t1s=[qubit_t1[q] for q in qubits]
    t2s=[qubit_t2[q] for q in qubits]

    qubit_durations_best = choose_best_for_duration(backend, t1s, t2s, candidate_durations)

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, sharex=True)

    fig.set_size_inches(10, 10)

    xs = [str(q) for q in qubits]

    ax_top.plot(xs, t1s, 'g-')
    ax_top.plot(xs, t2s, 'b-')

    legend = []
    for i, candidate in enumerate(candidate_durations):
        ax_bot.plot(xs,
                    [metric_func[metric](durations) for durations in candidate.values()],
                    '--')
        legend.append('%s compute on qubit (orientation %d)' % (metric, i))

    ax_bot.plot(xs,
                [metric_func[metric](durations) for durations in qubit_durations_best.values()],
                'c-')
    legend.append('%s compute on qubit (bestof)' % metric)

    if sample_circuit:
        ax_bot.plot(xs,
                    [durations[sample_circuit] for durations in candidate_durations[0].values()],
                    'y-')
        ax_bot.plot(xs,
                    [durations[sample_circuit] for durations in candidate_durations[1].values()],
                    'y-.')
        legend += ['%s sample circuit durations (orientation 0)' % metric, 
                   '%s sample circuit durations (orientation 1)' % metric]

    ax_bot.legend(legend,
                  loc='best')
    ax_top.legend(['qubit T1', 'qubit T2'])

    ax_top.set_title('QV%d circuits: variation in qubit busy time vs. coherence' % 2**len(qubits))

    ax_top.set_ylabel('T1/T2 (μs)')

    ax_bot.set_ylabel('length of computation (μs)')
    ax_bot.set_xlabel('qubit')

    # hide the spines between ax and ax2
    ax_top.spines['bottom'].set_visible(False)
    ax_bot.spines['top'].set_visible(False)

    # Make the spacing between the two axes a bit smaller
    plt.subplots_adjust(hspace=0.15)

    d = .015 # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax_top.transAxes, color='k', clip_on=False)
    ax_top.plot((-d,+d),(-d,+d), **kwargs) # top-left diagonal

    kwargs.update(transform=ax_bot.transAxes) # switch to the bottom axes
    ax_bot.plot((-d,d),(1-d,1+d), **kwargs) # bottom-right diagonal

    for x in range(len(qubits)):
        ax_bot.axvline(x=x, color='k')
        ax_top.axvline(x=x, color='k')

def pick_best_circuits_for_duration(backend, candidate_circuits, candidate_durations):
    qubits = list(candidate_durations[0].keys())
    num_circs = len(candidate_durations[0][qubits[0]])

    qubit_t1, qubit_t2 = get_t1_t2(backend, qubits)
    t1s=[qubit_t1[q] for q in qubits]
    t2s=[qubit_t2[q] for q in qubits]

    best_circuits = deepcopy(candidate_circuits[0])

    for sample_circuit in range(num_circs):
        circuit_cost = math.inf
        for durations, circuits in zip(candidate_durations, candidate_circuits):
            ds = [durations[q][sample_circuit] for q in qubits]
            cost = cost_durations_t1t2s(ds, t1s, t2s)
            if cost < circuit_cost:
                circuit_cost = cost
                best_circuits[sample_circuit] = circuits[sample_circuit]

    return best_circuits

def cost_cx_usages_fids(usages, fids):
    '''sum(usage*(1-fidelity)) over all cx.
    lower is better.'''
    return sum([u*(1-f/100) for u, f in zip(usages, fids)])

def choose_best_for_usage(backend, fids, candidate_link_usages):
    cmap = list(candidate_link_usages[0].keys())
    num_circs = len(candidate_link_usages[0][cmap[0]])

    link_usage_best = deepcopy(candidate_link_usages[0])

    for sample_circuit in range(num_circs):
        circuit_cost = math.inf
        for link_usages in candidate_link_usages:
            usages = [link_usages[tuple(l)][sample_circuit] for l in cmap]
            cost = cost_cx_usages_fids(usages, fids)
            if cost < circuit_cost:
                circuit_cost = cost
                for l in cmap:
                    link_usage_best[tuple(l)][sample_circuit] = link_usages[tuple(l)][sample_circuit]

    return link_usage_best

def plot_improvement_usage(backend, candidate_link_usages, sample_circuit=None, metric='average'):
    """Plot improvement due to picking a better layout orientation on a symmetrical topology.
    
    Args:
        backend (BaseBackend): a backend to get data (properties) from
        candidate_link_usages: candidate symmetries and CNOT usages associated with each (going to pick best)
        sample_circuit (int or None): show change for a particular circuit (None to omit)
        metric (str): 'average', 'median', 'max' or 'min'
    """
    metric_func = {
        'average': np.average,
        'median': np.median,
        'max': np.max,
        'min': np.min
    }

    cmap = list(candidate_link_usages[0].keys())
    link_fid = get_cx_errors(backend, cmap)
    fids = [link_fid[tuple(l)] for l in cmap]

    link_usages_best = choose_best_for_usage(backend, fids, candidate_link_usages)

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, sharex=True)

    fig.set_size_inches(10, 10)

    xs = [str(l) for l in link_fid.keys()]

    ax_top.plot(xs, fids, 'g-')

    legend = []
    for i, candidate in enumerate(candidate_link_usages):
        ax_bot.plot(xs,
                    [metric_func[metric](usages) for usages in candidate.values()],
                    'r--')
        legend.append('%s usage of CNOT (orientation %d)' % (metric, i))

    ax_bot.plot(xs,
                [metric_func[metric](usages) for usages in link_usages_best.values()],
                'c-')
    legend.append('%s usage of CNOT (bestof)' % metric)

    if sample_circuit:
        ax_bot.plot(xs,
                    [usages[sample_circuit] for usages in candidate_link_usages[0].values()],
                    'y-')
        ax_bot.plot(xs,
                    [usages[sample_circuit] for usages in candidate_link_usages[1].values()],
                    'y-.')
        legend += ['%s sample circuit CNOT usages (orientation 1)' % metric, 
                   '%s sample circuit CNOT usages (orientation 2)' % metric]

    ax_bot.legend(legend, loc='best')
    ax_top.legend(['CX error rate'])

    ax_top.set_title('QV%d circuits: variation in cx usage in circuits vs. cx fidelity' % 64)

    ax_top.set_ylabel('CX fidelity')

    ax_bot.set_ylabel('CX usage')
    ax_bot.set_xlabel('CX')

    # hide the spines between ax and ax2
    ax_top.spines['bottom'].set_visible(False)
    ax_bot.spines['top'].set_visible(False)

    # Make the spacing between the two axes a bit smaller
    plt.subplots_adjust(hspace=0.15)

    d = .015 # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax_top.transAxes, color='k', clip_on=False)
    ax_top.plot((-d,+d),(-d,+d), **kwargs) # top-left diagonal

    kwargs.update(transform=ax_bot.transAxes) # switch to the bottom axes
    ax_bot.plot((-d,d),(1-d,1+d), **kwargs) # bottom-right diagonal

    for x in range(len(cmap)):
        ax_bot.axvline(x=x, color='k')
        ax_top.axvline(x=x, color='k')
        
def cost_circuit_durations(d):
    '''just total circuit duration.
    lower is better.'''
    return d

def choose_best_for_circuit_duration(backend, candidate_circuit_durations):
    num_circs = len(candidate_circuit_durations[0])

    circuit_durations_best = deepcopy(candidate_circuit_durations[0])

    for sample_circuit in range(num_circs):
        circuit_cost = math.inf
        for durations in candidate_circuit_durations:
            d = durations[sample_circuit]
            cost = cost_circuit_durations(d)
            if cost < circuit_cost:
                circuit_cost = cost
                circuit_durations_best[sample_circuit] = durations[sample_circuit]

    return circuit_durations_best

def plot_improvement_circuit_duration(backend, candidate_circuit_durations, metric='average', qubits=None):
    """Plot improvement due to picking a better layout orientation on a symmetrical topology.
    
    Args:
        backend (BaseBackend): a backend to get data (properties) from
        candidate_circuit_durations: candidate symmetries and duration associated with each (going to pick best)
        sample_circuit (int or None): show change for a particular circuit (None to omit)
        metric (str): 'average', 'median', 'max' or 'min'
        qubits (list[int]): plot t1/t2 for those qubits
    """
    metric_func = {
        'average': np.average,
        'median': np.median,
        'max': np.max,
        'min': np.min
    }

    if not qubits:
        qubits=[1,2,3,4,5,6]
    qubit_t1, qubit_t2 = get_t1_t2(backend, qubits)
    t1s=[qubit_t1[q] for q in qubits]
    t2s=[qubit_t2[q] for q in qubits]

    circuit_durations_best = choose_best_for_circuit_duration(backend, candidate_circuit_durations)

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, sharex=True)

    fig.set_size_inches(10, 10)

    xs = [str(q) for q in qubits]

    ax_top.plot(xs, t1s, 'g-')
    ax_top.plot(xs, t2s, 'b-')

    legend = []
    for i, candidate in enumerate(candidate_circuit_durations):
        ax_bot.plot(xs,
                    [metric_func[metric](candidate)] * len(qubits),
                    'r--')
        legend.append('%s compute on qubit (orientation %d)' % (metric, i))

    ax_bot.plot(xs,
                [metric_func[metric](circuit_durations_best)] * len(qubits),
                'c-')
    legend.append('%s compute on qubit (bestof)' % metric)

    ax_bot.legend(legend,
                  loc='best')
    ax_top.legend(['qubit T1', 'qubit T2'])

    ax_top.set_title('QV%d circuits: variation in qubit busy time vs. coherence' % 2**len(qubits))

    ax_top.set_ylabel('T1/T2 (μs)')

    ax_bot.set_ylabel('length of computation (μs)')
    ax_bot.set_xlabel('qubit')

    # hide the spines between ax and ax2
    ax_top.spines['bottom'].set_visible(False)
    ax_bot.spines['top'].set_visible(False)

    # Make the spacing between the two axes a bit smaller
    plt.subplots_adjust(hspace=0.15)

    d = .015 # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax_top.transAxes, color='k', clip_on=False)
    ax_top.plot((-d,+d),(-d,+d), **kwargs) # top-left diagonal

    kwargs.update(transform=ax_bot.transAxes) # switch to the bottom axes
    ax_bot.plot((-d,d),(1-d,1+d), **kwargs) # bottom-right diagonal

    for x in range(len(qubits)):
        ax_bot.axvline(x=x, color='k')
        ax_top.axvline(x=x, color='k')
        
def pick_best_circuits_for_circuit_duration(backend, candidate_circuits, candidate_circuit_durations):
    num_circs = len(candidate_circuits[0])

    best_circuits = deepcopy(candidate_circuits[0])

    for sample_circuit in range(num_circs):
        circuit_cost = math.inf
        for durations, circuits in zip(candidate_circuit_durations, candidate_circuits):
            d = circuits[sample_circuit].duration
            cost = cost_circuit_durations(d)
            if cost < circuit_cost:
                circuit_cost = cost
                best_circuits[sample_circuit] = circuits[sample_circuit]

    return best_circuits