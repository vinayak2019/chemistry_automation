from fireworks.core.firework import Firework, Workflow
from files.task import *

def MyWorkflow():

    fw = Firework("your list of firetasks") # fireworks contains multiple firetask
    
    wf = Workflow("list of fireworks") # Workflow contains multiple fireworks

    return wf
