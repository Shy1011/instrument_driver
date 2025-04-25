from instrument_drivers.parent_classes.Multimeter import *

class DMM_KEYSIGHT_34461A(MULTIMEMTER):
    def __init__(self,device_id):
        super().__init__(device_id)

