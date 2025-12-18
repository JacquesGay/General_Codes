import numpy as np
import matplotlib.pyplot as plt

x,y = np.loadtxt('fes.dat', comments='#!', usecols=(0,1), unpack=True)

plt.plot(x,y)
plt.xlabel(r'Tyrosine Proton Ligand Distance (CV)')
plt.ylabel(r'Free Energy (kcal mol$^{-1}$)')

plt.show()
