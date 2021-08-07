from fireworks.core.firework import Firework, Workflow
from files.tasks import *

def MyWorkflow():

    fw = Firework("your list of firetasks") # fireworks contains multiple firetask
    
    wf = Workflow("list of fireworks") # Workflow contains multiple fireworks

    return wf


def SimpleWorkflow():
    f1 = Firework(OptimizationTask())  # fireworks contains multiple firetask
    f2 = Firework(HessianTask(),parents=[f1])
    f3 = Firework(TDHFTask(),parents=[f2])

    wf = Workflow([f1,f2,f3],name="SimpleWorkflow")  # Workflow contains multiple fireworks

    return wf


def ErrorRuntimeWorkflow():
    f1 = Firework(OptimizationErrorTask())  # fireworks contains multiple firetask
    f2 = Firework(HessianTask(), parents=[f1])
    f3 = Firework(TDHFTask(), parents=[f2])

    wf = Workflow([f1, f2, f3], name="ErrorRuntimeWorkflow")  # Workflow contains multiple fireworks

    return wf


def ErrorRaiseWorkflow():
    f1 = Firework(OptimizationTask())  # fireworks contains multiple firetask
    f2 = Firework(HessianErrorTask(), parents=[f1])
    f3 = Firework(TDHFTask(), parents=[f2])

    wf = Workflow([f1, f2, f3], name="ErrorRaiseWorkflow")  # Workflow contains multiple fireworks

    return wf

def DefuseWorkflow():
    f1 = Firework(OptimizationDefuseTask())  # fireworks contains multiple firetask
    f2 = Firework(HessianTask(), parents=[f1])
    f3 = Firework(TDHFTask(), parents=[f2])

    wf = Workflow([f1, f2, f3], name="DefuseWorkflow")  # Workflow contains multiple fireworks

    return wf


def PassParamsWorkflow():
    f1 = Firework(OptimizationPassParamsTask())  # fireworks contains multiple firetask
    f2 = Firework(HessianPassParamsTask(), parents=[f1])
    f3 = Firework(TDHFPassParamsTask(), parents=[f2])

    wf = Workflow([f1, f2, f3], name="PassParamsWorkflow")  # Workflow contains multiple fireworks

    return wf


def UserParamsWorkflow():
    f1 = Firework(OptimizationUserParamsTask(mol_coords="O 0. 0. 0.; H 0. -0.7 0.5; H 0. 0.7 0.5"))  # fireworks contains multiple firetask
    f2 = Firework(HessianPassParamsTask(), parents=[f1])
    f3 = Firework(TDHFPassParamsTask(), parents=[f2])

    wf = Workflow([f1, f2, f3], name="UserParamsWorkflow")  # Workflow contains multiple fireworks

    return wf


def Write2DBWorkfflow(basis):
    fw = Firework(HessianWrite2DBTask(basis=basis))
    wf = Workflow([fw], name="Write2DBWorkfflow_"+basis)  # Workflow contains multiple fireworks

    return wf
