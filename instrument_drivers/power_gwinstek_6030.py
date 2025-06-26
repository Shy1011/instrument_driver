from instrument_drivers.base.power import *
import time
class PowerGwinstek6030(Power) :
    def __init__(self,pInstruID):
        super().__init__(pInstruID)


    def turn_on_off(self,ch,switch):
        """
        :param ch: 1 / 2 / 3
        :param switch: "ON"/""OFF
        :return: none
        """

        self.instrument_write(f':OUTPut{ch}:STATe {switch}')  # 开启输出
        time.sleep(1)


    def read_voltage(self,ch):
        """

        :param ch: 1 / 2 / 3
        :return: float
        """

        voltage = self.instrument_query(f":MEASure{str(ch)}:VOLTage?")
        return float(voltage)

    def read_current(self,ch):
        """
        :param ch: 1 / 2 / 3
        :return: float
        """
        current = self.instrument_query(f":MEASure{str(ch)}:CURRent?")
        return float(current)

    def read_power(self, ch):
        """

        :param ch: 1 / 2 /3
        :return: float
        """
        power = self.instrument_query(f":MEASure{str(ch)}:POWer?")
        return float(power)

if __name__ == "__main__":

    power = PowerGwinstek6030("ASRL16::INSTR")
    power.set_volta_current(1,2,1)
    power.turn_on_off(1,"ON")
    print(power.read_voltage(1))
    print(power.read_current(1))
    print(power.read_power(1))

