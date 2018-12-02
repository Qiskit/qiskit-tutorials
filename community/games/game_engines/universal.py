import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import os
import copy
import networkx as nx

class layout:
    """Processing and display of data in ways that depend on the layout of a quantum device."""
    
    def __init__(self,num,coupling_map,pos):
        """The device for which we make the plot is specified by
        
        num = number of qubits
        coupling_map = list of possible cnots, each specified by a list of the two qubits involved 
        pos = dictionary for which qubits are keys and positions are values
        
        Rather than use the coupling map directly, we convert it into the `links` dictionary. This assigns a name to each coupling, to be used as keys. Labels for these links are also added to the `pos` dictionary.
        """
        
        self.num = num
        self.pos = pos
        self.links = {}
        char = 65
        for pair in coupling_map:
            self.links[chr(char)] = pair
            char += 1
        
        for pair in self.links:
            self.pos[pair] = [(self.pos[self.links[pair][0]][j] + self.pos[self.links[pair][1]][j])/2 for j in range(2)]

    def calculate_probs(self,raw_stats):
        """Given a counts dictionary as the input `raw_stats`, a dictionary of probabilities is returned. The keys for these are either integers (referring to qubits) or strings (referring to links of neighbouring qubits). For the qubit entries, the corresponding value is the probability that the qubit is in state `1`. For the pair entries, the values are the probabilities that the two qubits disagree (so either the outcome `01` or `10`."""
        Z = 0
        for string in raw_stats:
            Z += raw_stats[string]
        stats = {}
        for string in raw_stats:
            stats[string] = raw_stats[string]/Z
        
        probs = {}
        for n in self.pos:
            probs[n] = 0
        
        for string in stats:
            for n in range(self.num):
                if string[-n-1]=='1':
                    probs[n] += stats[string]
            for pair in self.links: 
                if string[-self.links[pair][0]-1]!=string[-self.links[pair][1]-1]:
                    probs[pair] += stats[string]
            
        return probs
        
    def matching(self,weights={}):
        
        if not weights:
            for pair in self.links:
                weights[pair] = random.random()
        
        G=nx.Graph()
        for pair in self.links:
            G.add_edge(self.links[pair][0],self.links[pair][1],weight=weights[pair])
            
        raw_pairs = nx.max_weight_matching(G, maxcardinality=True)
        
        pairs = []
        for pair in raw_pairs:
            pairs.append(list(pair))
        
        return pairs
      
    def plot(self,probs={},labels={},colors={},sizes={}):
        """An image representing the device is created and displayed.
        
        When no kwargs are supplied, qubits are labelled according to their numbers. The links of qubits for which a cnot is possible are shown by lines connecting the qubitsm, and are labelled with letters.
        
        The kwargs should all be supplied in the form of dictionaries for which qubit numbers and pair labels are the keys (i.e., the same keys as for the `pos` attribute).
        
        If `probs` is supplied (such as from the output of the `calculate_probs()` method, the labels, colors and sizes of qubits and links will be determined by these probabilities. Otherwise, the other kwargs set these properties directly."""                
        G=nx.Graph()
        
        for pair in self.links:
            G.add_edge(self.links[pair][0],self.links[pair][1])
            G.add_edge(self.links[pair][0],pair)
            G.add_edge(self.links[pair][1],pair)
        
        if probs:
            
            label_changes = copy.deepcopy(labels)
            color_changes = copy.deepcopy(colors)
            size_changes = copy.deepcopy(sizes)
            
            labels = {}
            colors = {}
            sizes = {}
            for node in G:
                if probs[node]>1:
                    labels[node] = ""
                    colors[node] = 'grey'
                    sizes[node] = 3000
                else:
                    labels[node] = "%.0f" % ( 100 * ( probs[node] ) )
                    colors[node] =( 1-probs[node],0,probs[node] )
                    if type(node)!=str:
                        if labels[node]=='0':
                            sizes[node] = 3000
                        else:
                            sizes[node] = 4000 
                    else:
                        if labels[node]=='0':
                            sizes[node] = 800
                        else:
                            sizes[node] = 1150
                                         
            for node in label_changes:
                labels[node] = label_changes[node]
            for node in color_changes:
                colors[node] = color_changes[node]      
            for node in size_changes:
                sizes[node] = size_changes[node]                   
                                        
        else:
            if not labels:
                labels = {}
                for node in G:
                    labels[node] = node
            if not colors:
                colors = {}
                for node in G:
                    if type(node) is int:
                        colors[node] = (node/self.num,0,1-node/self.num)
                    else:
                        colors[node] = (0,0,0)
            if not sizes:
                sizes = {}
                for node in G:
                    if type(node)!=str:
                        sizes[node] = 3000
                    else:
                        sizes[node] = 750

        # convert to lists, which is required by nx
        color_list = []
        size_list = []
        for node in G:
            color_list.append(colors[node])
            size_list.append(sizes[node])
        
        area = [0,0]
        for coord in self.pos.values():
            for j in range(2):
                area[j] = max(area[j],coord[j])
        for j in range(2):
            area[j] = (area[j] + 1 )*1.1
            
        if area[0]>2*area[1]:
            ratio = 0.65
        else:
            ratio = 1

        plt.figure(2,figsize=(2*area[0],2*ratio*area[1])) 
        nx.draw(G, self.pos, node_color = color_list, node_size = size_list, labels = labels, with_labels = True,
                font_color ='w', font_size = 18)
        plt.show() 