import pyvisa
from colorama import init, Fore, Style
"""
This is the base class for all instrument drivers.
"""

class Instrument():
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

    # def clear(self):
    #     "Reset the Device"
    #     "This command clears the event registers and queues."
    #     self.instrument.write("*CLS")

    def clear_get_event_status(self):
        " This command reads and clears the contents of the Standard Event Status Register."
        " Sometimes this command can also be used to clear the errors in the error queue."
        data = self.instrument.query("*CLS")
        return data

    def identify_instrument(self):
        "This command retrieves the identification string of the instrument."
        self.instrument.query("*IDN?")

    def trig(self):
        "This command generates a trigger event from a remote command interface."
        self.instrument.write("*TRG")

    def wait(self):
        "This command waits for all pending operations to complete."
        self.instrument.write("*WAI")

    def hint(self, tips):
        init(autoreset=True)
        print(Fore.RED)
        print(Fore.RED + "!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(Fore.RED + tips)
        print(Fore.RED + "!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def instrument_write(self, command: str) -> bool:
        """发送SCPI命令到仪器并处理错误队列

        在发送新命令前，会先检查并清空仪器的错误队列。
        任何非"No error"的错误信息都会被打印出来。

        Args:
            command: 要发送的SCPI命令字符串

        Returns:
            bool: 命令是否成功发送(True=成功, False=存在未处理错误)

        Raises:
            InstrumentError: 当仪器通信失败时抛出
        """
        try:
            # 清空错误队列
            while True:
                error_msg = self.instrument.query(':SYSTem:ERR?')   # Get the error message and clear the error queue
                if "No error" in error_msg:
                    break
                print(f"Instrument Error: {error_msg} (Last command: {self.recent_cmd})")

            # 记录并发送命令
            self.recent_cmd = f'write: {command}'
            self.instrument.write(command)
            return True

        except Exception as e:
            error_msg = f"Failed to send command '{command}': {str(e)}"
            self.recent_cmd = f'failed: {command}'
            print(error_msg)

    def instrument_query(self, command):
        """
        Query the instrument error queue.
        If the error message contains "No error", exit the loop.
        Otherwise, print the error message along with the
        most recent executed command (self.recent_cmd)
        for debugging purposes.

        :param command:
        :return: str
        """

        while m := self.instrument.query(':SYSTem:ERR?'):
            if "No error" in m:
                break
            print(m, f'recent: {self.recent_cmd}')
        result = self.instrument.query(command)  # Reset the instrument
        self.recent_cmd = f'query {command} recv {result}'
        return result

    def print_hints(self,sentence):
        print("\n--------------------------")
        print(sentence)
        print("\n--------------------------")



if __name__ == "__main__":
    dmm = Instrument("USB0::0x2A8D::0x1301::MY60099169::INSTR")