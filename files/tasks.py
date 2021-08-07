from fireworks.utilities.fw_utilities import explicit_serialize
from fireworks.core.firework import FiretaskBase, FWAction


@explicit_serialize
class MyFireTask(FiretaskBase):

    def run_task(self, fw_spec):

        # your code here
        pass



@explicit_serialize
class OptimizationTask(FiretaskBase):

    def run_task(self, fw_spec):
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


@explicit_serialize
class OptimizationErrorTask(FiretaskBase):

    def run_task(self, fw_spec):
        from pyscf import gto, scf
        from pyscf.geomopt.geometric_solver import optimize

        # build the molecule H20
        mol = gto.M(atom="water.xyz", basis="631g")

        # set the SCF calculations
        mf = scf.RHF(mol)

        # run the optimizer
        mol_eq = optimize(mf)

        # print the optimized coordinates
        print(mol_eq.atom_coords())



@explicit_serialize
class OptimizationDefuseTask(FiretaskBase):

    def run_task(self, fw_spec):
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

        if mol_eq.tot_electrons() > 2:
            return FWAction(defuse_children=True)


@explicit_serialize
class OptimizationPassParamsTask(FiretaskBase):

    def run_task(self, fw_spec):
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

        return FWAction(update_spec={"optimized_geometry": mol.tostring()})

@explicit_serialize
class OptimizationUserParamsTask(FiretaskBase):

    def run_task(self, fw_spec):
        from pyscf import gto, scf
        from pyscf.geomopt.geometric_solver import optimize

        # get molecule input from user
        mol_coords = self["mol_coords"]

        # build the molecule H20
        mol = gto.M(atom=mol_coords, basis="631g")

        # set the SCF calculations
        mf = scf.RHF(mol)

        # run the optimizer
        mol_eq = optimize(mf)

        # print the optimized coordinates
        print(mol_eq.atom_coords())

        return FWAction(update_spec={"optimized_geometry": mol.tostring()})




@explicit_serialize
class HessianTask(FiretaskBase):

    def run_task(self, fw_spec):

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


@explicit_serialize
class HessianErrorTask(FiretaskBase):

    def run_task(self, fw_spec):
        from pyscf import gto, scf
        from pyscf.hessian import thermo

        # build the molecule H20
        mol = gto.M(atom="O 0. 0. 0.; H 0. 0.657 0.587; H 0. 0.757 0.587", basis="631g")

        # Run SCF calculations
        mf = mol.RHF(mol).run()

        # compute the hessian
        hessian = mf.Hessian().kernel()

        # print the frequency data
        analysis_data = thermo.harmonic_analysis(mf.mol, hessian)
        print(analysis_data)

        if analysis_data["freq_error"] > 0:
            raise RuntimeError("Structure not optimized correctly. Has imaginary frequencies")



@explicit_serialize
class HessianPassParamsTask(FiretaskBase):

    def run_task(self, fw_spec):

        from pyscf import gto, scf
        from pyscf.hessian import thermo

        # get optimized molecule passed by previous task
        mol_string = fw_spec["optimized_geometry"]

        # build the molecule H20
        mol = gto.M()
        mol.fromstring(mol_string,"raw")
        mol.basis = '6-31G'

        # Run SCF calculations
        mf = mol.RHF(mol).run()

        # compute the hessian
        hessian = mf.Hessian().kernel()

        # print the frequency data
        print(thermo.harmonic_analysis(mf.mol, hessian))


@explicit_serialize
class HessianWrite2DBTask(FiretaskBase):

    def run_task(self, fw_spec):

        from pyscf import gto, scf
        from pyscf.hessian import thermo

        # get basis from user input
        basis = self["basis"]

        # build the molecule H20
        mol = gto.M(atom="O 0. 0. 0.; H 0. -0.757 0.587; H 0. 0.757 0.587", basis=basis)

        # Run SCF calculations
        mf = mol.RHF(mol).run()

        # compute the hessian
        hessian = mf.Hessian().kernel()

        # frequency data
        freq_info = thermo.harmonic_analysis(mf.mol, hessian)
        thermo_info = thermo.thermo(mf, freq_info["freq_au"], 298.15, 101325)

        data = {
            "G_tot" : thermo_info["G_tot"][0],
            "zero_point_energy" : thermo_info["ZPE"][0],
            "Cv_tot": thermo_info["Cv_tot"][0],
            "Cp_tot": thermo_info["Cp_tot"][0]
        }


        # connect to database with pymongo
        from pymongo import MongoClient

        client = MongoClient(" your host ") # copy the host value from my_launchpad.yaml
        db = client["fireworks"] # the database name
        collection = db["results"]  # the collection name

        # insert data into document
        collection.update_one({"_id": basis}, {"$set": data}, upsert=True)


@explicit_serialize
class TDHFTask(FiretaskBase):

    def run_task(self, fw_spec):
        from pyscf import gto, scf
        from pyscf.hessian import thermo

        # build the molecule H20
        mol = gto.M(atom="O 0. 0. 0.; H 0. -0.757 0.587; H 0. 0.757 0.587", basis="631g")

        # Run SCF calculations
        mf = mol.RHF(mol).run()

        # tdhf
        td = mf.TDHF().run()


@explicit_serialize
class TDHFPassParamsTask(FiretaskBase):

    def run_task(self, fw_spec):
        from pyscf import gto, scf
        from pyscf.hessian import thermo

        # get molecule from previous task
        mol_string = fw_spec["optimized_geometry"]

        # build the molecule H20
        mol = gto.M()
        mol.fromstring(mol_string)
        mol.basis = "6-31G"

        # Run SCF calculations
        mf = mol.RHF(mol).run()

        # tdhf
        td = mf.TDHF().run()


