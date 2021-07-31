from files.wflow import *
from fireworks import LaunchPad


# Generate the workflow
wf = MyWorkflow()

lpad = LaunchPad.from_file("my_launchpad.yaml")
lpad.add_wf(wf)

