from instrument_drivers.base.smu import *

class SmuKeithley2460(Smu):
    def __init__(self,device_id):
        super().__init__(device_id)
        self.v_range = {0.2,2,7,10,20,100,"auto"}
        self.i_range = {0.00001,0.0001,0.001,0.01,0.1,1,4,5,7, "auto"}

if __name__ == "__main__" :
    smu = SmuKeithley2460("USB0::0x05E6::0x2460::04624797::INSTR")
    default1 = ForceVoltSenseCurConfig()  # setup for SMU1
    default2 = ForceCurSenseVoltConfig()  # setup for SMU2

    default1.v_out = 0.2

    smu.force_volt_sens_cur_init(default1)
    smu.enable_output(True)
    smu.force_cur_sens_volt_init(default2)
    smu.enable_output(True)
    smu.enter_local_mode()

