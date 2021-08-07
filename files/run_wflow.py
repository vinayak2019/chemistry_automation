from files.wflow import *
from fireworks import LaunchPad

basis_set = ['sto-3g','321g','631g','cc-pvdz','def2-svp']


# Generate the workflow
wf = MyWorkflow()


lpad = LaunchPad.from_file("my_launchpad.yaml")
lpad.add_wf(wf)

