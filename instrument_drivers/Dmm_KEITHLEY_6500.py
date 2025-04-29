from instrument_drivers.base.Multimeter import *

class Dmm_KEITHLEY_6500(MULTIMEMTER):
    def __init__(self,device_id):
        super().__init__(device_id)

    def buzzer_ring(self, times):
        """
        Makes buzzer beep once.
        :return: none
        """
        print(f"This will make dmm ring {times} times")

if __name__ == "__main__":
    dmm = Dmm_KEITHLEY_6500("USB0::0x05E6::0x6500::04644817::INSTR")

    print(dmm.dc_voltage_measure("AUTO","AUTO"))
    print(dmm.dc_current_measure("AUTO","AUTO"))
    print(dmm.fre_measure())
    dmm.buzzer_ring(2)