from pyscf import gto, scf
from pyscf.hessian import thermo

# build the molecule H20
mol = gto.M(atom="O 0. 0. 0.; H 0. -0.757 0.587; H 0. 0.757 0.587", basis="631g")

# Run SCF calculations
mf = mol.RHF(mol).run()

# compute the hessian
hessian = mf.Hessian().kernel()

# print the frequency data
print(thermo.harmonic_analysis(mf.mol, hessian))
