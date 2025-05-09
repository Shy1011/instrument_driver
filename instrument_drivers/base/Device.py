import pyvisa
from colorama import init, Fore, Style
"""
This is the base class for all instrument drivers.
"""

class INSTRUMENT():
    def __init__(self, pInstruID):
        """
        actual object initial
        :param pRmObject: visa object name
        :param pInstruID: instrument ID
        """

        try:
            self.instrument = pyvisa.ResourceManager().open_resource(pInstruID)  # open instrument through instruID
            self.instrument.read_termination = "\n"
            self.instrument.timeout = 5000  # set instrument timeout
        except Exception as e:
            self.hint(f"Instrument ID {pInstruID} is not found")
            self.hint(f"Check your instrument connection or use another ID.")

    def reset(self):
        "Reset the Device"
        self.instrument.write("*RST")

    def identify_instrument(self):
        "Reset the Device"
        self.instrument.query("*IDN?")

    def hint(self, tips):
        init(autoreset=True)
        print(Fore.RED)
        print(Fore.RED + "!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(Fore.RED + tips)
        print(Fore.RED + "!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def instrument_write(self, command):
        """

        :param command:  str
        :return:
        """
        self.instrument.write(command)  # Reset the instrument

    def instrument_query(self, command):
        """

        :param command:
        :return: str
        """
        result = self.instrument.query(command)  # Reset the instrument

        return result

    def print_hints(self,sentence):
        print("\n--------------------------")
        print(sentence)
        print("\n--------------------------")



if __name__ == "__main__":
    dmm = INSTRUMENT("USB0::0x2A8D::0x1301::MY60099169::INSTR")