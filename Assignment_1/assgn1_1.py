#!/usr/bin/python3.5
from __future__ import print_function
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
        self.circ_start, self.circ_end = self.find_circuit()

        # self.circuit contains only the lines from start to end of circuit
        self.circuit = self.lines[self.circ_start+1: self.circ_end]
        print(self.circuit)

        #Analyze circuit
        self.analyze_circuit()

        #Print circuit
        self.print_reverse()

    def find_circuit(self):
        #Find the location of the circuit definition
        print('\nFinding circuit Definition')
        s1 = '.circuit'
        s2 = '.end'
        try:
            print('Circuit found from lines {0} to {1} (including .circuit and .end)'.format(self.lines.index(s1), self.lines.index(s2)))
        except:
            print('INVALID NETLIST FILE, .circuit/.end NOT FOUND')
            exit()
        if self.lines.index(s1) > self.lines.index(s2):
            print('.end found before .circuit')
            exit()
        return self.lines.index(s1), self.lines.index(s2)

    def analyze_circuit(self):
        print('\nAnalyzing circuit')
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
        print(self.circ_analysed)

    def print_reverse(self):
        print('\nPrinting in reverse')
        for i in reversed(self.circ_analysed):
            for j in reversed(i):
                print(j, end =' ')
            print('')

if __name__ == '__main__':
    if len(sys.argv) <> 2:
        print('Error in number of arguments, 1 filename expected')
    else:
        netfile = sys.argv[1]
        spice(netfile)
