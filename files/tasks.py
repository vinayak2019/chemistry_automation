from fireworks.utilities.fw_utilities import explicit_serialize
from fireworks.core.firework import FiretaskBase


@explicit_serialize
class MyFireTask(FiretaskBase):

    def run_task(self, fw_spec):

        # code here
        pass


