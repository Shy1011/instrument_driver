from instrument_drivers.base.multimeter import *
"""
This is the driver for GWINSTEK 9061 digital multimeter.
"""
class DmmGwinstek9061(Multimeter):
    def __init__(self,device_id):
        super().__init__(device_id)
        self.instrument.write("SENS:AVER:STAT OFF")  # cancel the digital filter only for GW 9061. otherwise the filter will cause an unstable reading


    def enter_local_mode(self):
        """
        Enter the local mode of the instrument.
        :return:
        """
        self.instrument_write(f"SYSTem:LOCal")


    def beep(self):
        """
        Beep the instrument.
        :return:
        """
        self.instrument_write(f"SYSTem:BEEPer")

    def enable_display(self,flag = 1):
        """
        Turn on/off the screen display of the instrument.
        仪器不显示时,会让测量变得更快
        :param flag:
        :return:
        """
        self.instrument_write(f"DISPlay {flag}")

    def display_text_on_screen(self,text : str = "Hello"):
        """
        Display text on the screen of the instrument.
        :param text:
        :return:
        """
        dmm.instrument_write(f"DISPlay:TEXT '{text}'")


if __name__ == "__main__":
    dmm = DmmGwinstek9061("USB0::0x2184::0x0059::GEW912502::INSTR")

    print(dmm.dc_voltage_measure())
    print(dmm.dc_current_measure())
    print(dmm.fre_measure())
