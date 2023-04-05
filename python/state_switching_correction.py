#This code accounts for state switching that occurs with excited state calculations

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 15:22:23 2022
State Switching Correction
@author: jgay15
"""

import os
import glob

def readFile(filename):  
    fileObj = open(filename, "r")
    lines = fileObj.read()
    fileObj.close()
    return lines


def sorting(filename):
    infile = open(filename, "r") #opens file with nrg and strng
    lines = []
    for line in infile:
        temp = line
        lines.append(temp)
        #print(temp)
    infile.close()
    lines.sort()
    print (type(lines))
    outfile = open("sorted.txt", "w")
    for i in lines:
            #j = " ".join(i)
            outfile.writelines(i)
            outfile.writelines("")
            #outfile.writelines('\n')
    outfile.close()

def index(filename, excited_state):
    k = 1
    with open(filename) as fn:
        lines = fn.read().splitlines()
    with open(filename, "w") as fn:
        for line in lines:
            if k < 11:
                k = str(k)
                print(line + "  Index " + k, file=fn)
                k = int(k)
                k = k + 1
            if k == excited_state + 1:
                k = 1

def project_file(excited_state):
    max_state=excited_state + 1
    file_loc = os.path.join ('log_files','*.log')  #searches for all .log
#print(file_loc)


    project_batch=glob.glob(file_loc)  #put in order command 
#print(project_batch)

    with open('projects.txt', 'w') as datafile: #opens file for writing
        for f in project_batch:
            project_id_1 = os.path.basename(f).split('.')[0]
            project_id = project_id_1.split('_')[2]
            with open(f, 'r') as outfile:
                data = outfile.readlines()
        
            job = 1
            for line in data:
                for i in range(1, max_state):
                    if f"Excited State   {i}" in line:
                        state_line = line
                        factors = state_line.split()
                        State_1 = factors[2]
                        State = State_1.split(':')[0]
                        Energy = factors[4]
                        Oscillator = factors[8]
                        oscstr = Oscillator.split('=')[1]
                        datafile.write('Project Batch {:>2}  job {:2}   Oscillator Strength {:2}   {:2} eV  Excited State  {:2}\n'.format(project_id, job, oscstr, Energy, State))
                    if 'Normal termination of Gaussian' in line:
                            job = job + 1
    datafile.close()

excited_state = int(input("Input number of excited states you wish to consider: \n"))

project_file(excited_state)

sorting('projects.txt')

index('sorted.txt', excited_state)
        
