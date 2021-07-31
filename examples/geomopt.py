from pyscf import gto, scf
from pyscf.geomopt.geometric_solver import optimize

# build the molecule H20
mol = gto.M(atom="O 0. 0. 0.; H 0. -0.7 0.5; H 0. 0.7 0.5", basis="631g")

# set the SCF calculations
mf = scf.RHF(mol)

# run the optimizer
mol_eq = optimize(mf)

# print the optimized coordinates
print(mol_eq.atom_coords())
