from instrument_drivers.base.SMU import *

class SmuKeithley2460(Smu):
    def __init__(self,device_id):
        super().__init__(device_id)
        self.v_range = {0.2,2,7,10,20,100,"auto"}
        self.i_range = {0.00001,0.0001,0.001,0.01,0.1,1,4,5,7, "auto"}

if __name__ == "__main__" :
    smu = SmuKeithley2460("USB0::0x05E6::0x2460::04624797::INSTR")


    smu.force_volt_sens_cur_init(0.1,1)
    smu.enable_output(True)
    smu.force_cur_sens_volt_init(0.1, 4)
    smu.enable_output(True)
    smu.enter_local_mode()

