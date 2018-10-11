# -*- coding: utf-8 -*-
"""Additional composite gates used in quantum tic tac toe"""

import numpy as np

def x_bus(qc,*bus):
    """Negates a whole bus"""
    for q in bus:
        qc.x(q)
        
def bus_or(qc,target,*busses):
    """Negates target if any of input busses is totally true, can add overall phase."""
    if len(busses)==1:
        qc.cnx(qc,*busses[0],target)
    elif len(busses) == 2:
        #negate everything
        qc.x_bus(qc,*busses[0],*busses[1],target)
        qc.ry(np.pi/4,target)
        qc.any_x(qc,*busses[1],target)
        qc.ry(np.pi/4,target)
        qc.any_x(qc,*busses[0],target)
        qc.ry(-np.pi/4,target)
        qc.any_x(qc,*busses[1],target)
        qc.ry(-np.pi/4,target)
        qc.x_bus(qc,*busses[0],*busses[1])
    elif len(busses) >= 3:
        qc.x_bus(qc,*busses[-1],target)
        qc.ry(np.pi/4,target)
        qc.any_x(qc,*busses[1],target)
        qc.ry(np.pi/4,target)
        #Recursiveness here:
        qc.bus_or(qc,target,*busses[:-1])
        qc.ry(-np.pi/4,target)
        qc.any_x(qc,*busses[1],target)
        qc.ry(-np.pi/4,target)
        qc.x_bus(qc,*busses[0],*busses[1])
        
def any_x(qc,*qubits):
    """Negate last qubit if any of initial qubits are 1."""
    qc.x_bus(qc,*qubits)
    qc.cnx(qc,*qubits)
    qc.x_bus(qc,*qubits[:-1])
        
def cry(qc,theta,q1,q2):
    """Controlled ry"""
    qc.ry(theta/2,q2)
    qc.cx(q1,q2)
    qc.ry(-theta/2,q2)
    qc.cx(q1,q2)
    
def cnx(qc,*qubits):
    """Control n-1 qubits, apply 'not' to last one
    Follows:
    @article{PhysRevA.52.3457,
      title = {Elementary gates for quantum computation},
      author = {Barenco, Adriano and Bennett, Charles H. and Cleve, Richard and DiVincenzo, David P. and Margolus, Norman and Shor, Peter and Sleator, Tycho and Smolin, John A. and Weinfurter, Harald},
      doi = {10.1103/PhysRevA.52.3457},
      url = {https://link.aps.org/doi/10.1103/PhysRevA.52.3457}
    }
    """
    if len(qubits) >= 3:
        last = qubits[-1]
        #A matrix: (decomposed cry also, control Ry)
        qc.crz(np.pi/2,qubits[-2],qubits[-1])
        #cry
        qc.cry(qc,np.pi/2,qubits[-2],qubits[-1])
        #Control
        qc.cnx(qc,*qubits[:-2],qubits[-1])
        #B matrix (cry again, but opposite angle)
        qc.cry(qc,-np.pi/2,qubits[-2],qubits[-1])
        #Control
        qc.cnx(qc,*qubits[:-2],qubits[-1])
        #C matrix
        qc.crz(-np.pi/2,qubits[-2],qubits[-1])
    elif len(qubits)==3:
        qc.ccx(*qubits)
    elif len(qubits)==2:
        qc.cx(*qubits)

if __name__ == "__main__":
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    from qiskit import CompositeGate, available_backends, execute

    q = QuantumRegister(5, "qr")
    q2 = QuantumRegister(1, "qr")
    print(len(q2))
    c = ClassicalRegister(5, "cr")
    qc = QuantumCircuit(q, c)
    qc.cry = cry
    qc.cnx = cnx
    qc.any_x = any_x
    qc.x_bus = x_bus
    qc.bus_or = bus_or

    #qc.h(q[0])
    qc.h(q[1])
    qc.h(q[2])
    qc.h(q[3])
    qc.h(q[-1])
    qc.bus_or(qc,q[0],[q[1],q[2],q[3]],[q[4]])

    qc.measure(q,c)
    job_sim = execute(qc, "local_qasm_simulator",shots=100)
    sim_result = job_sim.result()

    # Show the results
    print("simulation: ", sim_result)
    print(sim_result.get_counts(qc))
    print(qc.qasm())

