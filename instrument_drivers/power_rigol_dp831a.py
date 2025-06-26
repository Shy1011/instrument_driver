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
        assert ch in {"1", "2","3",1,2,3}, "DP831A Only has three Channels"
        self.instrument_write(f"OUTP CH{ch},{switch}")
        time.sleep(1)


    def read_voltage(self,ch) -> float :
        """

        :param ch: 1 / 2 / 3
        :return: float
        """
        assert ch in {"1", "2","3",1,2,3}, "DP831A Only has three Channels"
        voltage = self.instrument_query(f":MEASure:VOLTage? CH{ch}")

        return float(voltage)


    def read_current(self,ch)-> float :
        """
        :param ch: 1 / 2 / 3
        :return: float
        """
        assert ch in {"1", "2","3",1,2,3}, "DP831A Only has three Channels"
        current = self.instrument_query(f"MEASure:CURRent? CH{ch}")

        return float(current)


    def read_power(self,ch)-> float :
        """

        :param ch: 1 / 2 /3
        :return: float
        """
        assert ch in {"1", "2","3",1,2,3}, "DP831A Only has three Channels"
        power = self.instrument_query(f"MEASure:POWer? CH{ch}")

        return float(power)

    def beep(self):
        """
        让蜂鸣器 响一次
        :return:
        """
        self.instrument_write(f":SYSTem:BEEPer:IMMediate")

    def beeper_switch(self,switch : str = "OFF"):
        self.instrument_write(f"SYST:BEEP {switch}")

    def set_beightness_of_screen(self,brightness : int = 100):
        """
        设置屏幕亮度
        :param brightness:
        :return:
        """
        self.instrument_write(f":SYSTem:BRIGhtness {brightness}")

    def select_language(self,language : str = "ENG"):
        """
        选择语言  {EN|CH|JAP|KOR|GER|POR|POL|CHT|RUS}
        :param language:
        :return:
        """
        self.instrument_write(f":SYSTem:LANGuage:TYPE {language}")

    def back_to_local_mode(self):
        """
        返回本地模式
        :return:
        """
        self.instrument_write(f":SYSTem:LOCal")

    def lock_front_panel(self,switch : str = "OFF"):
        """
        锁定前端面板 防止误操作
        :param switch:
        :return:
        """
        self.instrument_write(f":SYSTem: LOCK {switch}")

    def display_mode(self,mode : str = "CLAS"):
        """
        设置显示模式  {NORMAL|MAX|MIN|OFF}
         NORMal：数字模式，以数字形式同时显示所有通道的电压、电流等参数。
         WAVE：波形模式，以波形和数字两种形式显示当前选中通道的电压、电流等参数。
         DIAL：表盘模式，以表盘和数字两种形式显示当前选中通道的电压、电流等参数。
         CLAS：经典模式，以数字（经典）形式同时显示所有通道的电压、电流等参数。
        :param mode:
        :return:
        """

        self.instrument_write(f":DISPlay:MODE {mode}")

    def display_switch(self,switch: str = "OFF"):
        """
        显示屏开关
        :param switch:
        :return:
        """
        self.instrument_write(f":DISP {switch}")

    def clear_strings_on_screen(self):
        """
        清除屏幕上的文字
        :return:
        """
        self.instrument_write(f":DISP:TEXT:CLE")

    def display_text_on_screen(self,text : str = "Hello World!"):
        """
        在屏幕上显示指定文字
        :param text:
        :return:
        """
        self.instrument_write(f':DISP:TEXT "{text}",25,35')




if __name__ == "__main__":

    power = PowerRigolDP831A("USB0::0x1AB1::0x0E11::DP8A242400223::INSTR")
    power.set_volta_current(3,2,1)
    power.turn_on_off(3,"ON")
    print(power.read_voltage(3))
    print(power.read_current(3))
    print(power.read_power(3))

