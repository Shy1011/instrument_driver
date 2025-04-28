from instrument_drivers.parent_classes.SMU import *

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
            pIout: float | str = 0.1,
            pVlimt: float | str = 5,
            pIrange: float | str = "auto",
            pVrange: float | str = "auto",
            pNplc: float | str = 1,
    ) -> None:
        assert pVrange in {0.2,2,7,10,20,100,"auto"}, "Paramemter v_range illegal"
        assert pIrange in {0.00001,0.0001,0.001,0.01,0.1,1,4,5,7, "auto"}, "Paramemter v_range illegal"
        super().force_cur_sens_volt_init()




if __name__ == "__main__" :
    smu = SMU("USB0::0x05E6::0x2460::04624797::INSTR")

    # smu.force_volt_sens_cur_init(1.85,0.1,"auto",0.1,1) # 1.85V Irange 100mA
    # smu.output_switch("ON")
    smu.force_cur_sens_volt_init(0, 10)

    smu.enter_local_mode()
    # smu.force_cur_sens_volt_init(0.1, 5)
    while True :
        data = input("Please Enter")
        if  data == "1.62" :
            smu.force_volt_sens_cur_init(1.62, 0.1, "auto", 0.1, 1)  # 1.85V Irange 100mA
            smu.output_switch("ON")
            smu.enter_local_mode()
            pass
        elif  data == "1.8" :
            smu.force_volt_sens_cur_init(1.8, 0.1, "auto", 0.1, 1)  # 1.85V Irange 100mA
            smu.output_switch("ON")
            smu.enter_local_mode()
            pass
        elif data == "1.98":
            smu.force_volt_sens_cur_init(1.98, 0.1, "auto", 0.1, 1)  # 1.85V Irange 100mA
            smu.output_switch("ON")
            smu.enter_local_mode()
        # elif data == "1.7":
        #     smu.force_volt_sens_cur_init(1.7, 0.1, "auto", 0.1, 1)  # 1.85V Irange 100mA
        #     smu.output_switch("ON")
        #     smu.enter_local_mode()
        elif data == "1.7":
            smu.force_volt_sens_cur_init(1.7, 0.008, "auto", 0.01, 1)  # 1.85V Irange 100mA
            smu.output_switch("ON")
            smu.enter_local_mode()
            input("Enter High Current Mode")
            smu.force_volt_sens_cur_init(1.7, 0.1, "auto", 0.1, 1)  # 1.85V Irange 100mA
            smu.output_switch("ON")
            smu.enter_local_mode()
        elif data == "off" or data == "OFF":
            smu.force_cur_sens_volt_init(0, 10) # off
            smu.output_switch("ON")
            smu.enter_local_mode()
        else:
            print("None,input incorrect")

