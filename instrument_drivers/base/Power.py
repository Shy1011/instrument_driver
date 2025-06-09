from instrument_drivers.base.Device import  *

"""
This is the base class for the power supply.

Develop a generic function for Power
"""
class Power(Instrument):
    def __init__(self, pInstruID):
        super().__init__(pInstruID)


    def set_volta_current(self,ch = 1,vol = 3.3,current = 1):
        """

        :param ch: 1 / 2 / 3
        :param vol:
        :param current:
        :return:
        """
        self.instrument.write(f"SOUR{ch}:VOLT {vol}")
        self.instrument.write(f"SOUR{ch}:CURR {current}")


    def turn_on_off(self,ch,switch):
        """
        :param ch: 1 / 2 / 3
        :param switch: "ON"/""OFF
        :return: none
        """
        print("Turn on/off the instrument")

    def read_voltage(self,ch):
        """

        :param ch: 1 / 2 / 3
        :return: float
        """
        print("read voltage")

        return float(0)


    def read_current(self,ch):
        """
        :param ch: 1 / 2 / 3
        :return: float
        """
        print("read current")

        return float(0)


    def read_power(self,ch):
        """

        :param ch: 1 / 2 /3
        :return: float
        """
        print("Read Power")

        return float(0)

    def sense_switch(self,ch,switch):
        """

        :param ch:  1 2 3 4
        :param switch: "ON" / "OFF"
        :return:
        """
        print("Sense On")
        pass

    def beeper_switch(self,switch):
        """

        :param switch: str  "ON" "OFF"
        :return:
        """
        print("Beeper")

    def hint(self,tips):
        init(autoreset=True)
        print(Fore.RED)
        print(Fore.RED+"!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(Fore.RED+tips)
        print(Fore.RED+"!!!!!!!!!!!!!!!!!!!!!!!!!!!")