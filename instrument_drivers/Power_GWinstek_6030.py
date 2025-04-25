from instrument_drivers.parent_classes.Power import *
import time
class Power_GWINSTEK_6030(Power) :
    def __init__(self,pInstruID):
        super().__init__(pInstruID)


    def turn_on_off(self,ch,switch):
        """
        :param ch: 1 / 2 / 3
        :param switch: "ON"/""OFF
        :return: none
        """

        self.instrument.write(f':OUTPut1:STATe {switch}')  # 开启输出
        time.sleep(1)


    def read_voltage(self,ch):
        """

        :param ch: 1 / 2 / 3
        :return: float
        """

        voltage = self.instrument.query(f":MEASure{str(ch)}:VOLTage?")
        return float(voltage)

    def read_current(self,ch):
        """
        :param ch: 1 / 2 / 3
        :return: float
        """
        current = self.instrument.query(f":MEASure{str(ch)}:CURRent?")
        return float(current)

    def read_power(self, ch):
        """

        :param ch: 1 / 2 /3
        :return: float
        """
        power = self.instrument.query(f":MEASure{str(ch)}:POWer?")
        return float(power)

if __name__ == "__main__":

    power = Power_GWINSTEK_6030("ASRL16::INSTR")
    power.set_volta_current(1,2,1)
    power.turn_on_off(1,"ON")
    print(power.read_voltage(1))
    print(power.read_current(1))
    print(power.read_power(1))

