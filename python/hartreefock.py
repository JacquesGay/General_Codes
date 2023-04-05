 import psi4 as p
 
 def simple_scf(molecule):
    #define molecule with current geometry
    p.molecule.update_geometry()



molecule mol {
0 1
O
H 1 1.0
H 1 1.0 2 104.5
symmetry c1
}

set {
basis sto-3g
scf_type direct
}

p.simple_scf(mol)
p.energy('scf')

#collect nuclear repulsion energy
p.print_out('Nuclear Repulsion Energy: %24.16f\n\n' % (Enuc))

#Generate the integrals
wfn = p.Wavefunction.build(mol, get_global_option("basis"))
mints = p.MintsHelper(wfn.basisset())
S = mints.ao_overlap()  #Overlap
T = mints.ao_kinetic()  #kinetic energy
V = mints.ao_Potential() #potential energy
I = mints.ao_eri()  #ERI Shell