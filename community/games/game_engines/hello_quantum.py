from qiskit import IBMQ
from qiskit import BasicAer as Aer
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import execute

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import copy
from ipywidgets import widgets  
from IPython.display import display, clear_output

try:
    IBMQ.load_accounts()
except:
    pass 

class run_game():
    # Implements a puzzle, which is defined by the given inputs.
    
    def __init__(self,initialize, success_condition, allowed_gates, vi, qubit_names, eps=0.1, backend=Aer.get_backend('qasm_simulator'), shots=1024,mode='circle',verbose=False):
        """
        initialize
            List of gates applied to the initial 00 state to get the starting state of the puzzle.
            Supported single qubit gates (applied to qubit '0' or '1') are 'x', 'y', 'z', 'h', 'ry(pi/4)'.
            Supported two qubit gates are 'cz' and 'cx'. Specify only the target qubit.
        success_condition
            Values for pauli observables that must be obtained for the puzzle to declare success.
        allowed_gates
            For each qubit, specify which operations are allowed in this puzzle. 'both' should be used only for operations that don't need a qubit to be specified ('cz' and 'unbloch').
            Gates are expressed as a dict with an int as value. If this is non-zero, it specifies the number of times the gate is must be used (no more or less) for the puzzle to be successfully solved. If the value is zero, the player can use the gate any number of times. 
        vi
            Some visualization information as a three element list. These specify:
            * which qubits are hidden (empty list if both shown).
            * whether both circles shown for each qubit (use True for qubit puzzles and False for bit puzzles).
            * whether the correlation circles (the four in the middle) are shown.
        qubit_names
            The two qubits are always called '0' and '1' from the programming side. But for the player, we can display different names.
        eps=0.1
            How close the expectation values need to be to the targets for success to be declared.
        backend=Aer.get_backend('qasm_simulator')
            Backend to be used by Qiskit to calculate expectation values (defaults to local simulator).
        shots=1024
            Number of shots used to to calculate expectation values.
        mode='circle'
            Either the standard 'Hello Quantum' visualization can be used (with mode='circle') or the alternative line based one (mode='line').
        verbose=False     
        """

        def get_total_gate_list():
            # Get a text block describing allowed gates.
            
            total_gate_list = ""
            for qubit in allowed_gates:
                gate_list = ""
                for gate in allowed_gates[qubit]:
                    if required_gates[qubit][gate] > 0 :
                        gate_list += '  ' + gate+" (use "+str(required_gates[qubit][gate])+" time"+"s"*(required_gates[qubit][gate]>1)+")"
                    elif allowed_gates[qubit][gate]==0:
                        gate_list += '  '+gate + ' '
                if gate_list!="":
                    if qubit=="both" :
                        gate_list = "\nAllowed symmetric operations:" + gate_list
                    else :
                        gate_list = "\nAllowed operations for " + qubit_names[qubit] + ":\n" + " "*10 + gate_list
                    total_gate_list += gate_list +"\n"
            return total_gate_list

        def get_success(required_gates):
            # Determine whether the success conditions are satisfied, both for expectation values, and the number of gates to be used.
            
            success = True
            grid.get_rho()
            if verbose:
                print(grid.rho)
            for pauli in success_condition:
                success = success and (abs(success_condition[pauli] - grid.rho[pauli])<eps)
            for qubit in required_gates:
                for gate in required_gates[qubit]:
                    success = success and (required_gates[qubit][gate]==0)
            return success

        def get_command(gate,qubit):
            # For a given gate and qubit, return the string describing the corresoinding Qiskit string.
            
            if qubit=='both':
                qubit = '1'
            qubit_name = qubit_names[qubit]
            for name in qubit_names.values():
                if name!=qubit_name:
                    other_name = name
            # then make the command (both for the grid, and for printing to screen)    
            if gate in ['x','y','z','h']:
                real_command  = 'grid.qc.'+gate+'(grid.qr['+qubit+'])'
                clean_command = 'qc.'+gate+'('+qubit_name+')'
            elif gate in ['ry(pi/4)','ry(-pi/4)']:
                real_command  = 'grid.qc.ry('+'-'*(gate=='ry(-pi/4)')+'np.pi/4,grid.qr['+qubit+'])'
                clean_command = 'qc.ry('+'-'*(gate=='ry(-pi/4)')+'np.pi/4,'+qubit_name+')'
            elif gate in ['cz','cx','swap']: 
                real_command  = 'grid.qc.'+gate+'(grid.qr['+'0'*(qubit=='1')+'1'*(qubit=='0')+'],grid.qr['+qubit+'])'
                clean_command = 'qc.'+gate+'('+other_name+','+qubit_name+')'
            return [real_command,clean_command]

        clear_output()
        bloch = [None]

        # set up initial state and figure
        grid = pauli_grid(backend=backend,shots=shots,mode=mode)
        for gate in initialize:
            eval( get_command(gate[0],gate[1])[0] )

        required_gates = copy.deepcopy(allowed_gates)

        # determine which qubits to show in figure
        if allowed_gates['0']=={} : # if no gates are allowed for qubit 0, we know to only show qubit 1
                shown_qubit = 1
        elif allowed_gates['1']=={} : # and vice versa
                shown_qubit = 0
        else :
                shown_qubit = 2

        # show figure
        grid.update_grid(bloch=bloch[0],hidden=vi[0],qubit=vi[1],corr=vi[2],message=get_total_gate_list())


        description = {'gate':['Choose gate'],'qubit':['Choose '+'qu'*vi[1]+'bit'],'action':['Make it happen!']}

        all_allowed_gates_raw = []
        for q in ['0','1','both']:
            all_allowed_gates_raw += list(allowed_gates[q])
        all_allowed_gates_raw = list(set(all_allowed_gates_raw))

        all_allowed_gates = []
        for g in ['bloch','unbloch']:
            if g in all_allowed_gates_raw:
                all_allowed_gates.append( g )
        for g in ['x','y','z','h','cz','cx']:
            if g in all_allowed_gates_raw:
                all_allowed_gates.append( g )
        for g in all_allowed_gates_raw:
            if g not in all_allowed_gates:
                all_allowed_gates.append( g )

        gate = widgets.ToggleButtons(options=description['gate']+all_allowed_gates)
        qubit = widgets.ToggleButtons(options=[''])
        action = widgets.ToggleButtons(options=[''])

        boxes = widgets.VBox([gate,qubit,action])
        display(boxes)
        if vi[1]:
            print('\nYour quantum program so far\n')
        self.program = []

        def given_gate(a):
            # Action to be taken when gate is chosen. This sets up the system to choose a qubit.
            
            if gate.value:
                if gate.value in allowed_gates['both']:
                    qubit.options = description['qubit'] + ["not required"]
                    qubit.value = "not required"
                else:
                    allowed_qubits = []
                    for q in ['0','1']:
                        if (gate.value in allowed_gates[q]) or (gate.value in allowed_gates['both']):
                            allowed_qubits.append(q)
                    allowed_qubit_names = []
                    for q in allowed_qubits:
                        allowed_qubit_names += [qubit_names[q]]
                    qubit.options = description['qubit'] + allowed_qubit_names

        def given_qubit(b):
            # Action to be taken when qubit is chosen. This sets up the system to choose an action.
            
            if qubit.value not in ['',description['qubit'][0],'Success!']:
                action.options = description['action']+['Apply operation']
                
        def given_action(c):
            # Action to be taken when user confirms their choice of gate and qubit.
            # This applied the command, updates the visualization and checks whether the puzzle is solved.
            
            if action.value not in ['',description['action'][0]]:
                # apply operation
                if action.value=='Apply operation':
                    if qubit.value not in ['',description['qubit'][0],'Success!']:
                        # translate bit gates to qubit gates
                        if gate.value=='NOT':
                            q_gate = 'x'
                        elif gate.value=='CNOT':
                            q_gate = 'cx'
                        else:
                            q_gate = gate.value
                        if qubit.value=="not required":
                            q = qubit_names['1']
                        else:
                            q = qubit.value
                        q01 = '0'*(qubit.value==qubit_names['0']) + '1'*(qubit.value==qubit_names['1']) + 'both'*(qubit.value=="not required")     
                        if q_gate in ['bloch','unbloch']:
                            if q_gate=='bloch':
                                bloch[0] = q01
                            else:
                                bloch[0] = None
                        else:
                            command = get_command(q_gate,q01)
                            eval(command[0])
                            if vi[1]:
                                print(command[1])
                            self.program.append( command[1] )
                        if required_gates[q01][gate.value]>0:
                            required_gates[q01][gate.value] -= 1

                        grid.update_grid(bloch=bloch[0],hidden=vi[0],qubit=vi[1],corr=vi[2],message=get_total_gate_list())

                success = get_success(required_gates)
                if success:
                    gate.options = ['Success!']
                    qubit.options = ['Success!']
                    action.options = ['Success!']
                    plt.close(grid.fig)
                else:
                    gate.value = description['gate'][0]  
                    qubit.options = ['']
                    action.options = ['']  

        gate.observe(given_gate)
        qubit.observe(given_qubit)
        action.observe(given_action)
        
        
class pauli_grid():
    # Allows a quantum circuit to be created, modified and implemented, and visualizes the output in the style of 'Hello Quantum'.

    def __init__(self,backend=Aer.get_backend('qasm_simulator'),shots=1024,mode='circle'):
        """
        backend=Aer.get_backend('qasm_simulator')
            Backend to be used by Qiskit to calculate expectation values (defaults to local simulator).
        shots=1024
            Number of shots used to to calculate expectation values.
        mode='circle'
            Either the standard 'Hello Quantum' visualization can be used (with mode='circle') or the alternative line based one (mode='line').    
        """
        
        self.backend = backend
        self.shots = shots
                
        self.box = {'ZI':(-1, 2),'XI':(-2, 3),'IZ':( 1, 2),'IX':( 2, 3),'ZZ':( 0, 3),'ZX':( 1, 4),'XZ':(-1, 4),'XX':( 0, 5)}
        
        self.rho = {}
        for pauli in self.box:
            self.rho[pauli] = 0.0
        for pauli in ['ZI','IZ','ZZ']:
            self.rho[pauli] = 1.0
            
        self.qr = QuantumRegister(2)
        self.cr = ClassicalRegister(2)
        self.qc = QuantumCircuit(self.qr, self.cr)
        
        self.mode = mode
        # colors are background, qubit circles and correlation circles, respectively
        if self.mode=='line':
            self.colors = [(1.6/255,72/255,138/255),(132/255,177/255,236/255),(33/255,114/255,216/255)]
        else:
            self.colors = [(1.6/255,72/255,138/255),(132/255,177/255,236/255),(33/255,114/255,216/255)]
        
        self.fig = plt.figure(figsize=(5,5),facecolor=self.colors[0])
        self.ax = self.fig.add_subplot(111)
        plt.axis('off')
        
        self.bottom = self.ax.text(-3,1,"",size=9,va='top',color='w')
        
        self.lines = {}
        for pauli in self.box:
            w = plt.plot( [self.box[pauli][0],self.box[pauli][0]], [self.box[pauli][1],self.box[pauli][1]], color=(1.0,1.0,1.0), lw=0 )
            b = plt.plot( [self.box[pauli][0],self.box[pauli][0]], [self.box[pauli][1],self.box[pauli][1]], color=(0.0,0.0,0.0), lw=0 )
            c = {}
            c['w'] = self.ax.add_patch( Circle(self.box[pauli], 0.0, color=(0,0,0), zorder=10) )
            c['b'] = self.ax.add_patch( Circle(self.box[pauli], 0.0, color=(1,1,1), zorder=10) )
            self.lines[pauli] = {'w':w,'b':b,'c':c}
                         
    
    def get_rho(self):
        # Runs the circuit specified by self.qc and determines the expectation values for 'ZI', 'IZ', 'ZZ', 'XI', 'IX', 'XX', 'ZX' and 'XZ'.
        
        bases = ['ZZ','ZX','XZ','XX']
        results = {}
        for basis in bases:
            temp_qc = copy.deepcopy(self.qc)
            for j in range(2):
                if basis[j]=='X':
                    temp_qc.h(self.qr[j])
            temp_qc.barrier(self.qr)
            temp_qc.measure(self.qr,self.cr)
            job = execute(temp_qc, backend=self.backend, shots=self.shots)
            results[basis] = job.result().get_counts()
            for string in results[basis]:
                results[basis][string] = results[basis][string]/self.shots
          
        prob = {}
        # prob of expectation value -1 for single qubit observables
        for j in range(2):
            for p in ['X','Z']:
                pauli = {}
                for pp in 'IXZ':
                    pauli[pp] = (j==1)*pp + p + (j==0)*pp
                prob[pauli['I']] = 0
                for basis in [pauli['X'],pauli['Z']]:
                    for string in results[basis]:
                        if string[(j+1)%2]=='1':
                            prob[pauli['I']] += results[basis][string]/2
        # prob of expectation value -1 for two qubit observables
        for basis in ['ZZ','ZX','XZ','XX']:
            prob[basis] = 0
            for string in results[basis]:
                if string[0]!=string[1]:
                    prob[basis] += results[basis][string]

        for pauli in prob:
            self.rho[pauli] = 1-2*prob[pauli]

    
    def update_grid(self,rho=None,labels=False,bloch=None,hidden=[],qubit=True,corr=True,message=""):
        """
        rho = None
            Dictionary of expectation values for 'ZI', 'IZ', 'ZZ', 'XI', 'IX', 'XX', 'ZX' and 'XZ'. If supplied, this will be visualized instead of the results of running self.qc.
        labels = None
            Dictionary of strings for 'ZI', 'IZ', 'ZZ', 'XI', 'IX', 'XX', 'ZX' and 'XZ' that are printed in the corresponding boxes.
        bloch = None
            If a qubit name is supplied, and if mode='line', Bloch circles are displayed for this qubit
        hidden = []
            Which qubits have their circles hidden (empty list if both shown).
        qubit = True
            Whether both circles shown for each qubit (use True for qubit puzzles and False for bit puzzles).
        corr = True
            Whether the correlation circles (the four in the middle) are shown.
        message
            A string of text that is displayed below the grid.
        """

        def see_if_unhidden(pauli):
            # For a given Pauli, see whether its circle should be shown.
            
            unhidden = True
            # first: does it act non-trivially on a qubit in `hidden`
            for j in hidden:
                unhidden = unhidden and (pauli[j]=='I')
            # second: does it contain something other than 'I' or 'Z' when only bits are shown
            if qubit==False:
                for j in range(2):
                    unhidden = unhidden and (pauli[j] in ['I','Z'])
            # third: is it a correlation pauli when these are not allowed
            if corr==False:
                unhidden = unhidden and ((pauli[0]=='I') or (pauli[1]=='I'))
            return unhidden

        def add_line(line,pauli_pos,pauli):
            """
            For mode='line', add in the line.
            
            line = the type of line to be drawn (X, Z or the other one)
            pauli = the box where the line is to be drawn
            expect = the expectation value that determines its length
            """
            
            unhidden = see_if_unhidden(pauli)
            coord = None
            p = (1-self.rho[pauli])/2 # prob of 1 output
            # in the following, white lines goes from a to b, and black from b to c
            if unhidden:
                if line=='Z':
                    a = ( self.box[pauli_pos][0], self.box[pauli_pos][1]+l/2 )
                    c = ( self.box[pauli_pos][0], self.box[pauli_pos][1]-l/2 )
                    b = ( (1-p)*a[0] + p*c[0] , (1-p)*a[1] + p*c[1] )
                    lw = 8
                    coord = (b[1] - (a[1]+c[1])/2)*1.2 + (a[1]+c[1])/2
                elif line=='X':
                    a = ( self.box[pauli_pos][0]+l/2, self.box[pauli_pos][1] )
                    c = ( self.box[pauli_pos][0]-l/2, self.box[pauli_pos][1] )
                    b = ( (1-p)*a[0] + p*c[0] , (1-p)*a[1] + p*c[1] )
                    lw = 9
                    coord = (b[0] - (a[0]+c[0])/2)*1.1 + (a[0]+c[0])/2
                else:
                    a = ( self.box[pauli_pos][0]+l/(2*np.sqrt(2)), self.box[pauli_pos][1]+l/(2*np.sqrt(2)) )
                    c = ( self.box[pauli_pos][0]-l/(2*np.sqrt(2)), self.box[pauli_pos][1]-l/(2*np.sqrt(2)) )
                    b = ( (1-p)*a[0] + p*c[0] , (1-p)*a[1] + p*c[1] )
                    lw = 9
                self.lines[pauli]['w'].pop(0).remove()
                self.lines[pauli]['b'].pop(0).remove()
                self.lines[pauli]['w'] = plt.plot( [a[0],b[0]], [a[1],b[1]], color=(1.0,1.0,1.0), lw=lw )
                self.lines[pauli]['b'] = plt.plot( [b[0],c[0]], [b[1],c[1]], color=(0.0,0.0,0.0), lw=lw )
                return coord
                         
        l = 0.9 # line length
        r = 0.6 # circle radius
        L = 0.98*np.sqrt(2) # box height and width
        
        if rho==None:
            self.get_rho()

        # draw boxes
        for pauli in self.box:
            if 'I' in pauli:
                color = self.colors[1]
            else:
                color = self.colors[2]
            self.ax.add_patch( Rectangle( (self.box[pauli][0],self.box[pauli][1]-1), L, L, angle=45, color=color) )  

        # draw circles
        for pauli in self.box:
            unhidden = see_if_unhidden(pauli)
            if unhidden:
                if self.mode=='line':
                    self.ax.add_patch( Circle(self.box[pauli], r, color=(0.5,0.5,0.5)) )
                else:
                    prob = (1-self.rho[pauli])/2
                    self.ax.add_patch( Circle(self.box[pauli], r, color=(prob,prob,prob)) )

        # update bars if required
        if self.mode=='line':
            if bloch in ['0','1']:
                for other in 'IXZ':
                    px = other*(bloch=='1') + 'X' + other*(bloch=='0')
                    pz = other*(bloch=='1') + 'Z' + other*(bloch=='0')
                    z_coord = add_line('Z',pz,pz)
                    x_coord = add_line('X',pz,px)
                    for j in self.lines[pz]['c']:
                        self.lines[pz]['c'][j].center = (x_coord,z_coord)
                        self.lines[pz]['c'][j].radius = (j=='w')*0.05 + (j=='b')*0.04
                px = 'I'*(bloch=='0') + 'X' + 'I'*(bloch=='1')
                pz = 'I'*(bloch=='0') + 'Z' + 'I'*(bloch=='1')
                add_line('Z',pz,pz)
                add_line('X',px,px)
            else:
                for pauli in self.box:
                    for j in self.lines[pauli]['c']:
                        self.lines[pauli]['c'][j].radius = 0.0
                    if pauli in ['ZI','IZ','ZZ']:
                        add_line('Z',pauli,pauli)
                    if pauli in ['XI','IX','XX']: 
                        add_line('X',pauli,pauli)
                    if pauli in ['XZ','ZX']:
                        add_line('ZX',pauli,pauli)
             
        self.bottom.set_text(message)
        
        if labels:
            for pauli in box:
                plt.text(self.box[pauli][0]-0.05,self.box[pauli][1]-0.85, pauli)
        
        self.ax.set_xlim([-3,3])
        self.ax.set_ylim([0,6])
        
        self.fig.canvas.draw()

