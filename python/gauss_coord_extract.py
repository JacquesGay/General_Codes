#Changes coordinates in Gaussian output file into an .xyz file

import sys
import re

#set global variables
opt_line = 0
start = 0
end = 0
opt_check = 'Optimization completed.'


# This comes from the input
# Gives the name to a possible new file

filename = sys.argv[1]
newfile = filename.split('.')[0] + ".xyz"

#open the original file in read mode
#create a new file with writing rights

openold=open(filename,"r")
opennew=open(newfile,"w")

#read the entire original file

rline = openold.readlines()

#Find optimized geometry
for l in range (len(rline)):
    if "Optimization Completed" in rline[l]:
        print("Geometry optimized")
        opt_line = int(rline.index(l))
        break
    elif l == int(len(rline)):
        print("Geometry not optimized")
        opennew.close()
        openold.close()
        exit()

for i in range (opt_line, len(rline)):
    if "Standard orientation:" in rline[i]:
        start = i
    for m in range (start + 5, len(rline)):
        if "---" in rline[m]:
            end = m
            break

# Conversion section
for line in rline[start+5 : end] :
    words = line.split()
    atoms = int(words[1])
    x_coord = str(words[3])
    y_coord = str(words[4])
    z_coord = str(words[5])

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
    opennew.write(F'{atoms} {x_coord} {y_coord} {z_coord} \n')
openold.close()
opennew.close()
