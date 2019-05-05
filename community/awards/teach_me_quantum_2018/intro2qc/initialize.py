from qiskit import *

class initialize:
    def __init__(self, circuit_name, qubit_number, bit_number, backend, shots):
        self.shots = shots    # the number of times the algorithm is going to be run 
        self.backend = backend # the backend selected to run the algorithm
        self.circ_name = circuit_name
        self.qubit_num = qubit_number 
        self.bit_num = bit_number
        
        # Define the specifcs of the quantum program
        
        # Create a quantum register. This will contain the qubits on which the algorithm is run
        self.q_reg = QuantumRegister(self.qubit_num,'q')
        
        # Create a classical register. This will store the result of measurements of the qubits
        self.c_reg = ClassicalRegister(self.bit_num,'c')
        
        # Create quantum circuit
        self.q_circuit = QuantumCircuit(self.q_reg,self.c_reg,name='test')
