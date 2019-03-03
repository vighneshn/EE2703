#!/usr/bin/python3.5
from __future__ import print_function
import numpy as np
import math
import cmath
import os
import sys

class spice:

    def __init__(self, filename):
        #validation file name in main
        try:
            with open(filename, 'r') as netfile:
                self.lines = netfile.readlines()
        except:
            print('FILE NOT FOUND')
            exit()
        #Take care of '\n' if present
        self.lines = [i.split('\n', 1)[0] for i in self.lines]
        self.w = 1e-7
        self.circ_start, self.circ_end = self.find_circuit()

        # self.circuit contains only the lines from start to end of circuit
        self.circuit = self.lines[self.circ_start+1: self.circ_end]

        #Analyze circuit
        self.analyze_circuit()

    def find_circuit(self):
        #Find the location of the circuit definition
        s1 = '.circuit'
        s2 = '.end'
        s3 = '.ac'
        try:
            print('Circuit found from lines {0} to {1} (including .circuit and .end)'.format(self.lines.index(s1), self.lines.index(s2)))
        except:
            print('INVALID NETLIST FILE, .circuit/.end NOT FOUND')
            exit()
        if self.lines.index(s1) > self.lines.index(s2):
            print('.end found before .circuit')
            exit()

        for x in self.lines:
            if '.ac' in x:
                self.w = float(x.split(' ')[-1])*2*math.pi

        return self.lines.index(s1), self.lines.index(s2)

    def analyze_circuit(self):
        self.circ_analysed = []
        for branch in self.circuit:
            analysed = branch.split(' ')
            # Remove the comment from the token
            comment_start_index = [analysed.index(i) for i in analysed if '#' in i]
            if comment_start_index <> []:
                del analysed[comment_start_index[0]:]
            #Removing unnecessary spaces being stored due to the split command
            while '' in analysed:
                analysed.remove('')
            #
            self.circ_analysed.append(analysed)

        ## Getting all unique node names, replacing them with numbers.
        unique_nodes = []
        for x in self.circ_analysed:
            if x[1] not in unique_nodes:
                unique_nodes.append(x[1])
            if x[2] not in unique_nodes:
                unique_nodes.append(x[2])
        #CONVENTION: current goes from lower indexed node to higher indexed node always.
        #Appending the current direction to the list, +1 or -1
        for x in self.circ_analysed:
            x[1] = unique_nodes.index(x[1])
            x[2] = unique_nodes.index(x[2])
            if x[1] > x[2]:
                x.append(-1)
            else:
                x.append(-1)

        # Found unique nodes
        print(self.circ_analysed)

        # Split into passive and active elements.
        self.active_v = []
        self.active_i = []
        self.passive = []
        for x in self.circ_analysed:
            if x[0][0] == 'R':
                self.passive.append(x)
            elif x[0][0] == 'L':
                x[3] = 1j*complex(float(x[3])*self.w)
                self.passive.append(x)
            elif x[0][0] == 'C':
                x[3] = -1j/complex(float(x[3])*self.w)
                self.passive.append(x)
            elif x[0][0] == 'V':
                self.active_v.append(x)
            elif x[0][0] == 'I':
                self.active_i.append(x)

        M,b = self.create_matrix(unique_nodes)
        print(M)
        print(b)

        soln = self.solve(M,b)
        #print([soln[i], unique_nodes[i] for i in range(len(unique_nodes))], [soln[i], self.active_v[i-unique_nodes] for i in range(len(unique_nodes), b.size)])
        for i in range(len(soln)):
            if i < len(unique_nodes):
                #print("V at ",unique_nodes[i], " is ", soln[i][0])
                print("V at ",unique_nodes[i], " is ", cmath.polar(soln[i]))
            else:
                print("I through from ",unique_nodes[self.active_v[i-len(unique_nodes)][1]],"to", unique_nodes[self.active_v[i-len(unique_nodes)][2]],"through ", self.active_v[i-len(unique_nodes)][0], " is ", cmath.polar(soln[i][0]))

    def create_matrix(self, unique_nodes):
        M = np.zeros((len(unique_nodes)+len(self.active_v),len(unique_nodes)+len(self.active_v)), dtype = complex)
        b = np.zeros((len(unique_nodes)+len(self.active_v),1), dtype = complex)

        print(unique_nodes)
        for i in range(len(unique_nodes)):
            for x in self.passive:
                ##Now x[4] is redundant, can replace it with one.
                if i == x[1]:
                    M[i][x[1]] = M[i][x[1]] - x[4]/complex(x[3])
                    M[i][x[2]] = M[i][x[2]] + x[4]/complex(x[3])
                elif i == x[2]:
                    M[i][x[1]] = M[i][x[1]] + x[4]/complex(x[3])
                    M[i][x[2]] = M[i][x[2]] - x[4]/complex(x[3])
            for x in self.active_i:
                if i == x[1]:
                    b[i] = b[i] - float(x[3])
                elif i == x[2]:
                    b[i] = b[i] + float(x[3])
            
        for i in range(len(unique_nodes),b.size):
            x = self.active_v[i-len(unique_nodes)]
            print(i,' ',x[1],' ',x[2])
            M[i][x[1]] = M[i][x[1]] - 1
            M[i][x[2]] = M[i][x[2]] + 1
    
            M[x[1]][i] = M[x[1]][i] + 1
            M[x[2]][i] = M[x[2]][i] - 1
            if x[3] == 'dc':
                b[i] = b[i] + float(x[4])
            elif x[3] == 'ac':
                b[i] = b[i] + complex(x[4])*(math.cos(float(x[5]))+1j*math.sin(float(x[5])))/2

        ## Need to pop one of the nodes and and the equation Vgnd = 0
        M[0,:] = 0
        M[0,unique_nodes.index('GND')] = 1
        b[0] = 0
        return M,b

    def solve(self, M, b):
        x = np.linalg.solve(M,b)
        return x

if __name__ == '__main__':
    if len(sys.argv) <> 2:
        print('Error in number of arguments, 1 filename expected')
    else:
        netfile = sys.argv[1]
        spice(netfile)
