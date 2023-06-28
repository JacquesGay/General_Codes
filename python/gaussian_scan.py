"""
Pull optimized coordinates and SCF energy between atoms of interest from each scan length
"""

import sys
import numpy as np
import os

#set global variables
opt_line = []
orientation_start = []
orientation_end = []
energies = []
distances = []

def geompull(input, geomoutput, distoutput, numatoms):
    #set local variables
    #opt_line = []
    opt_line_length = 0
    #orientation_start = []
    #orientation_end = []
    numberatoms = numatoms
    #end = 0
    #opt_check = 'Optimization completed'
    
    #open the input for reading and open the output for writing

    opennew = open(geomoutput, 'w')
    opendistfile = open(distoutput, 'w')  #THIS FILE WILL ONLY BE USED FOR DISTANCE COMPUTATION
    print(input)
    with open(input, "r") as f:
        rline = f.readlines()


    #read through the oldfile and find optimizations
    for n, l in enumerate(rline):
        #print(n, l)
        if "optimization completed" in l.lower(): #CHANGE TO STATIONARY POINT FOUND 
            opt_line.append(n)
        elif "Gaussian calculation successful!".lower() in l.lower():
            opt_line_length = len(opt_line)
            print("All geometries pulled. Number of Geometries = " + str(opt_line_length))
            break
        elif n == int(len(rline)):
            print("Optimized Geometry Not Found")
            opennew.close()
            exit()

    geom_index = 0


    for value in opt_line:
        count = value
        for j in rline[value:]:
            if "Standard orientation:".lower() in j.lower():
                orientation_start.append(count)
                break
            count += 1
        for m in range (orientation_start[geom_index] + 5, len(rline)): ############This may be an issue
            if "---" in rline[m]:
                orientation_end.append(m)
                break
        geom_index += 1


    end_index = 0

    for value in orientation_start:
        opennew.write(F'{numberatoms} \n \n')
        count = 1
        for line in rline[value+5 : orientation_end[end_index]]:
            words = line.split()
            atoms = int(words[1])
            if atoms == 1:
                atoms = "H"
            elif atoms == 6:
                atoms = "C"
            elif atoms == 7:
                atoms = "N"
            elif atoms == 8:
                atoms = "O"
            elif atoms == 15:
                atoms = "P"
            x_coord = str(words[3])
            y_coord = str(words[4])
            z_coord = str(words[5])
            opendistfile.write(F'0{count}) {atoms} {x_coord} {y_coord} {z_coord} \n')  #For the distance file
            opennew.write(F'{atoms} {x_coord} {y_coord} {z_coord} \n')  #for the geometry file we will use
            count += 1
        end_index += 1
        opendistfile.write(F'\n \n')
        #opennew.write(F'\n \n')
    opennew.close()
    opendistfile.close()

def energypull(input, output):
    with open(input, "r") as f:
        rline = f.readlines()
    energydoc = open(output, 'w')
    index=0

    for value in opt_line:
        count = value
        for line in rline[value-900:orientation_end[index]]:
            if "SCF Done".lower() in line.lower():
                words = line.split()
                energy = str(words[4])
                energies.append(energy)
                energydoc.write(F'Geometry {index +1}: {energy} A.U. \n \n')
            #elif int(count) == int(orientation_end[index]):
            #    print("No energy found, please increase searching range")
            #    energydoc.close()
            #    break
            #count += 1
        index += 1
    energydoc.close()
        
def computedist(input, output, atom1, atom2):
    d1 = []
    d2 = []
    a1 = "0"+atom1 + ")"
    a2 = "0"+atom2 + ")"
    distances = []
    with open(os.path.join(sys.path[0], input), "r") as f:
        dlines = f.readlines()
    defile = open(output, 'w')
    for line in dlines:
        if a1 in line:
            words1 = line.split()
            d1.extend([float(words1[2]), float(words1[3]), float(words1[4])])
        elif a2 in line:
            words2 = line.split()
            d2.extend([float(words2[2]), float(words2[3]), float(words2[4])])
    arrayleng = len(d2) / 3
    arr1 = np.array(d1)
    arr2 = np.array(d2)
    arr1 = np.split(arr1, arrayleng)
    arr2 = np.split(arr2, arrayleng)
    arr1 = np.transpose(arr1)
    arr2 = np.transpose(arr2)
    for i in range(0,11):
        p1 = np.array([arr1[0][i], arr1[1][i], arr1[2][i]])
        p2 = np.array([arr2[0][i], arr2[1][i], arr2[2][i]])
        #print(p1,p2)
        dist = np.linalg.norm(p1-p2)
        distances.append(dist)
    print(distances)
    print(energies)

    for i in range(0,11):
        defile.write(F'Distance: {distances[i]} Energy: {energies[i]} \n')

    defile.close()


filename = sys.argv[1]
newfile = filename.split('.')[0] + ".xyz"
distfile = "dist_" + filename.split('.')[0] + ".txt"
energyfile = "energy.txt"
disenergfile = "dist_and_energy_" + filename.split('.')[0] + ".txt"

numberofatoms=input('Number of atoms in system:')

natom1, natom2 = input('First Atom Number:'), input('Second Atom Number:')

geompull(filename, newfile, distfile, numberofatoms)

energypull(filename,energyfile)

computedist(distfile,disenergfile,natom1,natom2)

if os.path.isfile(distfile):
    os.remove(distfile)

if os.path.isfile(energyfile):
    os.remove(energyfile)
