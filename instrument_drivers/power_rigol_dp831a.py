import time

from instrument_drivers.base.power import *

class PowerRigolDP831A(Power):
    def __init__(self,pInstruID):
        super().__init__(pInstruID)



    def turn_on_off(self,ch,switch):
        """
        turn on specific channels
        :param ch: 1 / 2 / 3
        :param switch: "ON"/""OFF
        :return: none
        """
        assert range in {"1", "2","3"}, "DP821A Only has three Channels"
        self.instrument.write(f"OUTP CH{ch},{switch}")
        time.sleep(1)

    def read_voltage(self,ch):
        """

        :param ch: 1 / 2 / 3
        :return: float
        """
        assert range in {"1", "2", "3"}, "DP821A Only has three Channels"
        voltage = self.instrument.query(f":MEASure:VOLTage? CH{ch}")

        return float(voltage)


    def read_current(self,ch):
        """
        :param ch: 1 / 2 / 3
        :return: float
        """
        assert range in {"1", "2", "3"}, "DP821A Only has three Channels"
        current = self.instrument.query(f"MEASure:CURRent? CH{ch}")

        return float(current)


    def read_power(self,ch):
        """

        :param ch: 1 / 2 /3
        :return: float
        """
        assert range in {"1", "2", "3"}, "DP821A Only has three Channels"
        power = self.instrument.query(f"MEASure:POWer? CH{ch}")

        return float(power)


if __name__ == "__main__":

    power = PowerRigolDP831A("USB0::0x1AB1::0x0E11::DP8A242400223::INSTR")
    power.set_volta_current(3,2,1)
    power.turn_on_off(3,"ON")
    print(power.read_voltage(3))
    print(power.read_current(3))
    print(power.read_power(3))

