from instrument_drivers.base.smu import *

class SmuKeithley2450(Smu):
    def __init__(self,device_id):
        super().__init__(device_id)
        self.v_range = {0.02,0.2,2,20,200,"auto"}
        self.i_range = {0.00001, 0.0001, 0.001, 0.01, 0.1, 1, "auto"}


if __name__ == "__main__" :
    smu = SmuKeithley2450("USB0::0x05E6::0x2450::04576516::INSTR")

    default1 = ForceVoltSenseCurConfig()  # setup for SMU1
    default2 = ForceCurSenseVoltConfig()  # setup for SMU2

    default1.v_out = 0.2

    smu.force_volt_sens_cur_init(default1)
    smu.enable_output(True)
    smu.force_cur_sens_volt_init(default2)
    smu.enable_output(True)
    smu.enter_local_mode()
