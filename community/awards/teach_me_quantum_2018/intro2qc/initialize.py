from qiskit import *

class initialize:
    def __init__(self, circuit_name, qubit_number, bit_number, backend, shots):
        self.shots = shots    # the number of times the algorithm is going to be run 
        self.backend = backend # the backend selected to run the algorithm
        self.circ_name = circuit_name
        self.qubit_num = qubit_number 
        self.bit_num = bit_number
        
        # Define the specifcs of the quantum program
        QPS_SPECS = {
            'circuits': [{
                'name': self.circ_name, # name of quantum circuit
                'quantum_registers': [{
                    'name':'q', # name of quantum register
                    'size': qubit_number # size of quantum register
                }],
                'classical_registers': [{
                    'name':'c', # name of classical register
                    'size': bit_number # size of classical register
                }]}],
        }

        #Create a quantum program with the specifics define above

        self.Q_program = QuantumProgram(specs=QPS_SPECS)


        #Create a quantum register. This will contain the qubits on which the algorithm is run

        self.q_reg = self.Q_program.get_quantum_register('q')


        #Create a classical register. This will store the result of measurements of the qubits

        self.c_reg = self.Q_program.get_classical_register('c')

        #Create quantum circuit

        self.q_circuit = self.Q_program.get_circuit(self.circ_name)
