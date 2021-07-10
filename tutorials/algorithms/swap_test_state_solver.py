
# Importing standard Qiskit libraries
from math import pi,sin,cos,asin,acos,sqrt,ceil
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.compiler import transpile, assemble
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller
import random


backend = Aer.get_backend('statevector_simulator')
backend2 = Aer.get_backend('qasm_simulator')


# creating a SWAP test circuit which can be later appended to any circuit
swap_circuit = QuantumCircuit(3)
swap_circuit.h(0)
swap_circuit.cswap(0,1,2)
swap_circuit.h(0)
swap_circuit.draw()


def create_state(qc,i,theta=None, phi=None, mode='u'):
    '''
    Creates a general qubit state given by the parameters of bloch sphere at a qubit of given quantum circuit.
    
    Parameters:
    qc : Quantum circuit of the qubit
    i : Index of the qubit in qc which is to be transformed to a general state
    theta : Angle from z-axis in bloch sphere, if None then takes a random value in the range [0,pi]
    phi : Phase angle from x-axis in bloch sphere, if None then takes a random value in the range [0,2*pi]
    mode : Uses single u3 gate (which is more efficient) by default to create the state, else if mode is 'rot' then uses separate rotation about y and z axis in the bloch sphere
    '''
    if theta==None:
        theta = pi*random.randrange(0,1001)/1000
    if phi==None:
        phi = 2*pi*random.randrange(0,1001)/1000
    if mode=='u':
            qc.u(theta, phi, 0, i)
    elif mode=='rot':
        qc.ry(theta,i)
        qc.rz(phi,i)
        
        
def variational_circuit(theta=None, phi=None):
    '''
    Returns a quantum circuit consisting of 1 qubit that creates a general qubit state given by the parameters of bloch sphere at that qubit.
    
    Parameters:
    theta : Angle from z-axis in bloch sphere, if None then takes a random value in the range [0,pi]
    phi : Phase angle from x-axis in bloch sphere, if None then takes a random value in the range [0,2*pi]
    
    Returns:
    qc : A QuantumCircuit of size 1 qubit that is in a general state given by the parameters of the bloch sphere (theta and phi).
    ''' 
    qc = QuantumCircuit(1)
    create_state(qc,0,theta,phi)
    return qc

def create_prod_state(qc, s=None, start_qubit=0):
    '''
    Creates a product state at first n-qubits of quantum circuit given by the binary string.
    
    Parameters:
    qc : Quantum circuit of the qubits
    s : Binary string representing the multi-qubit product state
    start_qubit : The qubit from which the creation of product state needs to start
    '''
    for i,k in enumerate(s):
        if int(k):
            qc.x(i + start_qubit)
        
        
def swap_test(state1=(0,0), state2=(0,0), n=5000):
    '''
    Finds the probability of '0' state in the ancilla qubit after creating the desired system states (those which 
    needs to be tested) on the given quantum circuit and appending a swap test circuit at the desired positions.
    
    Parameters:
    state1 : Tuple containing parameters (theta1,phi1) in bloch sphere which describe the state of q1
    state2 : Tuple containing parameters (theta2,phi2) in bloch sphere which describe the state of q2 
    n : number of shots
    
    Returns:
    prob_zero : A float number containing the probability to measure ancilla qubit in stat |0> for n shots 
    '''
    qc = QuantumCircuit(3,1)
    if(state1[0] or state1[1]):
        create_state(qc,1,state1[0],state1[1])
    if(state2[0] or state2[1]):
        create_state(qc,2,state2[0],state2[1])
    qc=qc+swap_circuit
    qc.measure(0,0)
    
    counts = execute(qc,backend2,shots=n).result().get_counts()
    if('0' in counts):
        prob_zero = counts['0']/n
    else:
        prob_zero = 0.0
        
    return prob_zero


def qubit_state_solver_singlebasis(theta = None, phi = None):
    '''
    Finds the best choice of parameters (theta, phi) using SWAP test to reproduce the given general state or a randomly generated state of a single qubit.
    
    Parameters:
    theta : angle from z-axis in bloch sphere, if None then takes a random value in the range [0,pi]
    phi : phase angle from x-axis in bloch sphere, if None then takes a random value in the range [0,2*pi]
    
    Returns (tuple of 2 tuples):
    qubit_state: tuple containing the given or randomly genrated parameters (theta, phi).
    pred_state: tuple containing the predicted parameters (pred_theta, pred_phi) using SWAP test.
    '''
    pred_theta = 0
    pred_phi = 0
    
    # Make a quantum circuit to predict the value of theta using SWAP test
    prob_zero = swap_test((theta,phi))
    pred_theta = 2*acos(sqrt(max(0,(2*prob_zero-1))))

    # Make a quantum circuit to predict the value of phi using SWAP test 
    prob_zero = swap_test((theta,phi),(pred_theta, 0))
    pred_phi = acos(min(1,max(-1,(4*(prob_zero-1)/((sin(pred_theta))**2))+1)))
    
    # Now there can be two possible values of pred_phi, which are 2*pi - pred_phi or pred_phi itself as 
    # both will give the same result in SWAP test
    # Make two quantum circuits to check the correct value of phi using separate SWAP test on both the posssible values 
    prob1 = swap_test((theta,phi),(pred_theta, pred_phi))
    prob2 = swap_test((theta,phi),(pred_theta, 2*pi - pred_phi))
    if (prob1<prob2):
        pred_phi = 2*pi - pred_phi
        
    #Return the parameters
    qubit_state = (theta,phi)
    pred_state = (pred_theta,pred_phi)
    print(f'Qubit State : {qubit_state}\nPredicted State : {pred_state}')

    return qubit_state,pred_state

def qubit_state_solver_multibasis(theta = None, phi = None):
    '''
    Finds the best choice of parameters (theta, phi) using SWAP test in X, Y and Z basis to reproduce the given general state or a randomly generated state of a single qubit.
    
    Parameters:
    theta : angle from z-axis in bloch sphere, if None then takes a random value in the range [0,pi]
    phi : phase angle from x-axis in bloch sphere, if None then takes a random value in the range [0,2*pi]
    
    Returns (tuple of 2 tuples):
    qubit_state: tuple containing the given or randomly genrated parameters (theta, phi).
    pred_state: tuple containing the predicted parameters (pred_theta, pred_phi) using SWAP test.
    '''  
    pred_theta = 0
    pred_phi = 0
    
    # Make a quantum circuit to predict the value of theta using SWAP test in Z basis
    qc_theta = QuantumCircuit(3,1)
    create_state(qc_theta,1,theta,phi)
    qc_theta=qc_theta+swap_circuit
    qc_theta.measure(0,0)
    
    counts = execute(qc_theta,backend2,shots=5000).result().get_counts()
    prob_zero = counts['0']/5000
    pred_theta = 2*acos(sqrt(max(0,(2*prob_zero-1))))
    
    # Make a quantum circuit to predict the value of theta using SWAP test in X basis
    qc_phi = QuantumCircuit(3,1)
    create_state(qc_phi, 1, theta, phi)
    qc_phi.h(1)
    qc_phi=qc_phi+swap_circuit
    qc_phi.measure(0,0)
    
    counts = execute(qc_phi,backend2,shots=5000).result().get_counts()
    prob_zero = counts['0']/5000
    pred_phi = 2*acos(sqrt(max(0,(2*prob_zero-1))))
    
    # Now there can be two possible values of pred_phi, 
    # which are 2*pi - pred_phi or pred_phi itself as both will give the same result in SWAP test
    
    # Make a quantum circuit to predict the value of theta using SWAP test in Y basis to confirm the correct value of phi.
    # If probability of measuring the ancilaa qubit in |0> is more than or equal to 75% (let's say with 0.005% error),  
    # the predicted value of phi is correct else it should be changed to (2*pi - pred_phi)
    qc = QuantumCircuit(3,1)
    create_state(qc, 1, theta, phi)
    qc.u(pi/2,0,pi/2,1) # Can use 1 u gate with these parameters instead of an S-dagger and a Hadamard gate
    qc = qc + swap_circuit
    qc.measure(0,0)
    
    counts = execute(qc,backend2,shots=5000).result().get_counts()
    prob_zero = counts['0']/5000
    if prob_zero<0.74:
        pred_phi=(2*pi - pred_phi)
    
    qubit_state = (theta,phi)
    pred_state = (pred_theta,pred_phi)
    print(f'Qubit State : {qubit_state}\nPredicted State : {pred_state}')
    
    return ( qubit_state,pred_state)

def general_qubit_state_solver(theta = None, phi = None, multi=False):
    '''
    Finds the best choice of parameters (theta, phi) using SWAP test to reproduce the given general state or a randomly generated state of a single qubit. 
    
    If incomplete or no quantum state is passed as arguments, a general single qubit state is randomly created using the create_state() function.
    
    Parameters:
    theta : angle from z-axis in bloch sphere, if None then takes a random value in the range [0,pi]
    phi : phase angle from x-axis in bloch sphere, if None then takes a random value in the range [0,2*pi]
    multi : the number of basis to be used for SWAP testing. By default False indicates single (Z) basis is used 
    which needs 4 SWAP tests to find the correct values of parameters (theta, phi), less efficient but less error. 
    If True then all three (X, Y and Z) basis are used it needs only 3 SWAP test but more error prone.
    '''
    #Setting the initial values of parameters 
    if (theta==None or phi==None):
        theta = pi*random.randrange(0,1001)/1000
        phi = 2*pi*random.randrange(0,1001)/1000
    
    if(multi):
        qubit_state_solver_multibasis(theta, phi)
    else:
        qubit_state_solver_singlebasis(theta, phi)
        

def prod_state_finder_individual_swap(n,s,k):
    '''
    Finds the product state using individual ancilla qubit for each qubit by qubit SWAP test. 
    
    Parameters:
    n : Number of qubits in the quantum product state
    s : Binary string representing the given n-qubit product state
    k : Maximum no. of states that can be SWAP tested in one circuit
    Returns:
    s : Binary string representing the given n-qubit product state
    pred_s : Binary string representing the predicted n-qubit product state
    '''
    pred_state = [0]*n
    pred_s=''

    for i in range(ceil(n/k)): # loop until all qubits are measured
        qc = QuantumCircuit(2*k+n,k)
        create_prod_state(qc,s)

        for j in range(k): # SWAP test maximum qubits possible
            if(k*i+j<n):
                qc = qc.compose(swap_circuit,[n+k+j,n+j,k*i+j])
                qc.measure(n+k+j,k-1-j)

        counts = execute(qc,backend2,shots=5000).result().get_counts()
        for key in counts: # Add the counts to respective qubits which are in |0> state
            for qubit in range(len(key)):
                if key[qubit] == '0' and k*i+qubit<n:
                    pred_state[k*i+qubit] += counts[key] 

    for state in pred_state: # Check the probability and determine the predicted state
        state = state/5000
        state = max(state,0.5)
        if 1-state<state-0.5:
            pred_s = pred_s + '0'
        else:
            pred_s = pred_s + '1'

    print(f'Qubit State : {s}\nPredicted State : {pred_s}')
    return s,pred_s
    
    
def prod_state_finder_grid_search(n,s):
    '''
    Finds the product state using only one ancilla qubit for the SWAP test and grid search over all possible product states with n qubits. 
    
    Parameters:
    n : Number of qubits in the quantum product state
    s : Binary string representing the given n-qubit product state
    
    Returns:
    s : Binary string representing the given n-qubit product state
    pred_s : Binary string representing the predicted n-qubit product state
    '''
    pred_s=''

    # Grid search over 2^n possible product states
    for i in range(2**n):
        pred_s = format(i,'0'+str(n)+'b')
        qc = QuantumCircuit(2*n+1, 1)
        create_prod_state(qc,s)
        create_prod_state(qc,pred_s,n)

        # Add SWAP circuit
        qc.h(2*n)
        for j in range(n):
            qc.cswap(2*n,j,n+j)
        qc.h(2*n)
        qc.measure(2*n,0)

        counts = execute(qc,backend2,shots=5000).result().get_counts()
        prob_zero = counts['0']/5000
        if 1-prob_zero<prob_zero-0.5:
            break

    print(f'Qubit State : {s}\nPredicted State : {pred_s}')
    return s,pred_s


def prod_state_reconstruct(n, s=None, max_qubits=27, grid_search=False):
    '''
    Finds the product state using qubit by qubit SWAP test with n qubits. 
    
    Parameters:
    n : Number of qubits in the quantum product state
    s : Binary string representing the given n-qubit product state, if None then takes a random value
    max_qubits : Maximum number of qubits (including system and ancilla) that can be used for conducting the SWAP tests 
    
    Returns:
    qc : QuantumCircuit with n-qubits representing the reconstructed (predicted) product state 
    s : Binary string representing the given n-qubit product state
    pred_s : Binary string representing the predicted n-qubit product state
    '''
    if s==None:
        s=''
        for _ in range(n):
            s=s+str(random.randrange(0,2))
    pred_s = ''
    
    if grid_search:
        if max_qubits<n*2 +1:
            print("Insufficient number of qubits for grid search")
        else:
            s,pred_s = prod_state_finder_grid_search(n,s)
    
    else:
        if max_qubits<n+2:
            print("Insufficient number of qubits for qubit by qubit SWAP tests")
        else:
            k=min((max_qubits-n)//2,n) #maximum no. of states that can be SWAP tested in one circuit
            s,pred_s = prod_state_finder_individual_swap(n,s,k)
    
    qc = QuantumCircuit(n)
    create_prod_state(qc,pred_s)
    
    return qc,s,pred_s
             