from instrument_drivers.base.SMU import *

class Smu_Keithley_2460(SMU):
    def __init__(self,device_id):
        super().__init__(device_id)

    def force_volt_sens_cur_init(self,
             v_out: float | str = 0,
             i_limit: float | str = 1,
             v_range: float | str = "auto",
             i_range: float | str = "auto",
             nplc=1):

        assert v_range in {0.2,2,7,10,20,100,"auto"},"Paramemter v_range illegal"
        assert i_range in {0.00001,0.0001,0.001,0.01,0.1,1,4,5,7, "auto"}, "Paramemter v_range illegal"
        super().force_volt_sens_cur_init(v_out,i_limit,v_range,i_range,nplc)

    def force_cur_sens_volt_init(
            self,
            i_out: float | str = 0.1,
            v_limit: float | str = 5,
            i_range: float | str = "auto",
            v_range: float | str = "auto",
            nplc: float | str = 1,
    ) -> None:
        assert v_range in {0.2, 2, 7, 10, 20, 100, "auto"}, "Paramemter v_range illegal"
        assert i_range in {0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 4, 5, 7, "auto"}, "Paramemter v_range illegal"
        super().force_cur_sens_volt_init()




if __name__ == "__main__" :
    smu = SMU("USB0::0x05E6::0x2460::04624797::INSTR")


    smu.force_volt_sens_cur_init(0.1,1)
    smu.enable_output(True)
    smu.force_cur_sens_volt_init(0.1, 4)
    smu.enable_output(True)
    smu.enter_local_mode()

