#!/usr/bin/env python3

"""
Created on Fri Jun 10 08:30:17 2022
Basis 
@author: jgay15
This script calculates basis functions for an input molecule
This requires the Atomic_Basis_Functions.csv
"""

import chemparse
import numpy as np
import pandas as pd
import csv

def find_index(input):
        o = open('Atomic_Basis_Functions.csv')
        myData = csv.reader(o)
        index = 0
        for row in myData:
            #print(row)
            if row[0] == input:
                return index
            else : index+=1

def split(chemistry):
    parsedchem=chemparse.parse_formula(chemistry)
    atoms = []
    stoich = []
    items = parsedchem.items()
    for item in items:
        atoms.append(item[0])
        stoich.append(item[1])
    atoms = np.array(atoms)
    stoich = np.array(stoich)
    length = len(atoms)
    return atoms, stoich, length

chemform=input("Please enter the reduced chemical formula. \nNote: Capitalization matters; ie. Krypton must be written as Kr and carbon must be written as C. \n")

basis=input("Please type the basis set you would like to run. \nNote: Please use standard basis input. \nie. STO-3G instead of sto3g or sto-3g.\n")

basis_index = find_index(basis)-1
#print(basis_index)
#print(basis_index)

atoms, stoich, length = split(chemform)

sum = 0
df = pd.read_csv('Atomic_Basis_Functions.csv')


values=[]
stop = 0
for i in range(0, length):
    atom = atoms[i]
   #stoich = stoich[i]
    if str(df.loc[basis_index,atom]) == 'nan':
        stop = stop + 1
        break
    else:
       bv = float(df.loc[basis_index,atom])
       tb = bv*stoich[i]
       values.append(tb)


if stop == 1:
    print("This basis set is not available for selected molecule/atom")
else:
    for i in range(0,len(values)):
        sum = sum + values[i]
    print(sum)
