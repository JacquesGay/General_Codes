"""
Pull optimized coordinates and SCF energy between atoms of interest from each scan length
"""

import sys
import re

#set global variables
opt_line = []
orientation_start = []
orientation_end = []

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
        for line in rline[value+5 : orientation_end[end_index]]:
            words = line.split()
            atoms = int(words[1])
            x_coord = str(words[3])
            y_coord = str(words[4])
            z_coord = str(words[5])
            opendistfile.write(F'{atoms} {x_coord} {y_coord} {z_coord} \n')  #For the distance file

            if atoms == 1:
                atoms == "H"
            elif atoms == 6:
                atoms == "C"
            elif atoms == 7:
                atoms == "N"
            elif atoms == 8:
                atoms == "O"
            elif atoms == 15:
                atoms == "P"
            
            opennew.write(F'{atoms} {x_coord} {y_coord} {z_coord} \n')  #for the geometry file we will use
        end_index += 1
        opendistfile.write(F'\n \n')
        opennew.write(F'\n \n')
    opennew.close()
    opendistfile.close()

def energypull(input, output):
    with open(input, "r") as f:
        rline = f.readlines()
    energydoc = open(output, 'w')
    index=0

    for value in opt_line:
        count = value
        for line in rline[value-1000:orientation_end[index]]:
            if "SCF Done".lower() in line.lower():
                words = line.split()
                energy = str(words[4])

                energydoc.write(F'Geometry {index +1}: {energy} A.U. \n \n')
            #elif int(count) == int(orientation_end[index]):
            #    print("No energy found, please increase searching range")
            #    energydoc.close()
            #    break
            #count += 1
        index += 1
    energydoc.close()
        


    


filename = sys.argv[1]
newfile = filename.split('.')[0] + ".xyz"
distfile = "dist_" + filename.split('.')[0] + ".txt"
energyfile = "energy.txt"

geompull(filename, newfile, distfile, 59)

energypull(filename,energyfile)
