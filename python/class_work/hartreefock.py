#### This code requires psithon
import numpy as np
import scipy

def simple_scf(molecule):
    MAXITER = 50 #Number of allowed iterations
    E_conv = 1.0e-10 #difference criteria for convergence

    molecule.update_geometry() #updates to most recent geometry

    #Get charge, multiplicity and number of electrons
    charge = molecule.molecular_charge()
    mult = molecule.multiplicity()
    Z = 0
    for A in range(molecule.natom()):
        Z += molecule.Z(A)
    ndocc = int(Z/2) - int(charge / 2) #number of doubly-occupied orbitals
    E_nuc = molecule.nuclear_repulsion_energy()

    #Check multiplicity is equal to one
    if mult != 1:
        print("multiplicity is not singlet")
        exit()
    else:
        print("multiplicity is singlet")

    wfn = Wavefunction.build(molecule, get_global_option("basis"))
    mints = MintsHelper(wfn.basisset())

    ##################Get the one-electron integrals as matrices##############
    S = np.asarray(mints.ao_overlap()) #Overlap integrals
    T = np.asarray(mints.ao_potential()) #Kinetic Energy integrals
    V = np.asarray(mints.ao_kinetic()) #Potential Energy Integrals
    I = np.asarray(mints.ao_eri()) #ERI tesnor
    #Construct hamiltonian
    H = np.add(T, V)

    #Get number of basis functions
    nbf = np.shape(S)[0]

    ######Construct orthoganizing matrix#####
    #Make the matrices and vectors required for diagonalization
    #diagonilize S
    lam, U = np.linalg.eigh(S)
    lam = np.diag(lam)
    #form S^-1/2 matrix
    lam_half = scipy.linalg.fractional_matrix_power(lam,-0.5)
    #U_trans = np.matrix.transpose(U)
    S_half_1 = np.matmul(U, lam_half)
    S_half = np.matmul(S_half_1, U.T)

    #################Construct initial (guess) density matrix###########
    #Construct core fock matrix in orthogonalized basis
    F_i_1 = np.matmul(S_half.T, H)
    F_i = np.matmul(F_i_1, S_half)
    #Diagonalize fock matrix using a standard eigenvalue routine with scipy; E = enegergy matrix, C = coefficient matrix
    E, C = np.linalg.eigh(F_i)
    #C = np.diag(C)
    #Form original eigenvector matrix
    C_0 = np.matmul(S_half,C)
    #from C_0 get the orbitals that are occupied and ommit unoccupied
    C_occ = C_0[:,:ndocc]
    #Build density matrix from the occupied orbitals
    D = np.einsum('ui,vi->uv', C_occ, C_occ, optimize=True)

    ####Begin SCF#######
    SCF_E = 0.0
    E_old = 0.0

    #Begin loop
    for scf_iter in range(1, MAXITER +1):
        #Form new fock matrix
        J = np.einsum('uvrs,rs->uv', I, D, optimize=True)
        K = np.einsum('urvs,rs->uv', I, D, optimize=True)
        F = H + 2*J - K

        #Get electronic energy
        SCF_E = np.einsum('uv,vu->', (H+F), D, optimize=True) + E_nuc

        #Get difference in energy
        dE = E_old - SCF_E
        print(F'SCF Iteration : {scf_iter} Energy = {SCF_E} dE = {dE}')

        #Check convergence
        if (abs(SCF_E - E_old) < E_conv):
            break
        E_old = SCF_E

        #Transform fock matrix
        F_prime_0 = np.matmul(S_half.T, F)
        F_prime = np.matmul(F_prime_0, S_half)
      

        #Diagonalize the fock matrix
        E_prime, C_prime = scipy.linalg.eigh(F_prime, overwrite_a = False, eigvals_only = False)
        #C_prime = np.diag(C_prime)

        #Construct new SCF eignvector matrix
        C_prime_0 = S_half.dot(C_prime)

        #Get new occupied orbitals
        C_prime_occ = C_prime_0[:,:ndocc]

        #Form new density matrix
        D = np.einsum('ui,vi->uv', C_prime_occ, C_prime_occ, optimize=True)

        #Check what iteration the code is on. If it has reached max iterations stop it
        if (scf_iter == MAXITER):
            psi4.core.clean()
            raise Exception("Maximum number of SCF iterations exceeded.")

    print('\nSCF converged.')
    print('Final RHF Energy: %.8f Ha' % (SCF_E))

molecule mol {
O
H 1 1.0
H 1 1.0 2 104.5
symmetry c1
}

set {
basis sto-3g
}

simple_scf(mol)
set scf_type direct
energy('scf') 
