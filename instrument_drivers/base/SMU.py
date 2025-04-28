import time

import pyvisa
from colorama import init, Fore,Style
from instrument_drivers.base.Device import  *
class SMU(INSTRUMENT):
    def __init__(self, pInstruID):
        super().__init__(pInstruID)

    def force_volt_sens_cur_init(self, v_out : float|str = 0, i_limit : float | str = 1, v_range : float | str ="auto", i_range : float | str ="auto", nplc=1) -> None:
        """
        配置设备为电压源输出、电流测量模式（Force Voltage, Sense Current）

        参数：
            pVout (float/str): 电压源输出值（单位：V）
            pIlimt (float): 电压源模式下的电流限值（单位：A）
            pVrange (float/str): 电压源量程，数值为具体量程，字符串表示自动量程
            pIrange (float/str): 电流测量量程，数值为具体量程，字符串表示自动量程
            pNplc (float): 电流测量的积分时间（NPLC值）

        返回：
            None
        """

        """
        配置电压源输出+电流测量模式（Force Voltage, Sense Current）
    
        参数：
            v_out (float): 输出电压值(V)
            i_limit (float): 电流限值(A)
            v_range (float/str): 电压量程值(float)或"auto"(默认)
            i_range (float/str): 电流量程值(float)或"auto"(默认)
            nplc (float): 积分周期数(默认1)
        """
        # 电压源配置
        self.instrument.write(":SOUR:FUNC VOLT")
        self.instrument.write(f":SOUR:VOLT {v_out}")

        # 量程设置（三目运算符简化）
        v_range_cmd = ":SOUR:VOLT:RANG:AUTO ON" if isinstance(v_range, str) else f":SOUR:VOLT:RANG {v_range}"
        i_range_cmd = ":SENS:CURR:RANG:AUTO ON" if isinstance(i_range, str) else f":SENS:CURR:RANG {i_range}"

        self.instrument.write(f":SOUR:VOLT:ILIM {i_limit}")
        self.instrument.write(v_range_cmd)
        self.instrument.write(":SENS:FUNC 'CURR'")
        self.instrument.write(i_range_cmd)
        self.instrument.write(f":SENS:CURR:NPLC {nplc}")

        self.instrument.write(f":SOUR:VOLT:ILIM {i_limit}")
        self.instrument.write(v_range_cmd)
        self.instrument.write(":SENS:FUNC 'CURR'")
        self.instrument.write(i_range_cmd)
        self.instrument.write(f":SENS:CURR:NPLC {nplc}")


    def force_cur_sens_volt_init(
            self,
            pIout: float | str = 0.1,
            pVlimt: float | str = 5,
            pIrange: float | str = "auto",
            pVrange: float | str = "auto",
            pNplc: float | str = 1,
    ) -> None:
        """
        配置 SMU（源测量单元）为 ​**强制电流模式（Force Current）​**，并设置 ​**电压测量（Sense Voltage）​**。

        Args:
            pIout (float | str): 强制输出的电流值（单位：A），例如 `0.1` 或 `"100e-3"`。
            pVlimt (float | str): 强制电流模式下的电压限制（单位：V），例如 `10.0` 或 `"10"`。
            pIrange (float | str): 电流量程（数值或 `"AUTO"`），例如 `1.0` 或 `"AUTO"`。
            pVrange (float | str): 电压测量量程（数值或 `"AUTO"`），例如 `10.0` 或 `"AUTO"`。
            pNplc (float | str): 电压测量的积分时间（NPLC），例如 `1` 或 `"10"`。

        Returns:
            None
        """
        # --- 源代码配置 ---
        self.instrument.write(":SOUR:FUNC CURR")  # 设置 SMU 源模式为电流输出
        self.instrument.write(f":SOUR:CURR:LEV {pIout}")  # 设置强制输出电流值
        self.instrument.write(f":SOUR:CURR:VLIM {pVlimt}")  # 设置电流模式下的电压限制

        # 设置电流量程（自动或固定值）
        if isinstance(pIrange, str) and pIrange.upper() == "AUTO":
            self.instrument.write(":SOUR:CURR:RANG:AUTO ON")
        else:
            self.instrument.write(f":SOUR:CURR:RANG {pIrange}")

        # --- 测量配置 ---
        self.instrument.write(":SENS:FUNC 'VOLT'")  # 设置 SMU 测量模式为电压

        # 设置电压量程（自动或固定值）
        if isinstance(pVrange, str) and pVrange.upper() == "AUTO":
            self.instrument.write(":SENS:VOLT:RANG:AUTO ON")
        else:
            self.instrument.write(f":SENS:VOLT:RANG {pVrange}")

        self.instrument.write(f":SENS:VOLT:NPLC {pNplc}")  # 设置电压测量的积分时间（NPLC）

    def enable_4wire_mode(self,switch : str = "OFF") -> None:
        """启用 4-Wire 测量模式（不改变其他配置）"""
        self.instrument.write(f":SYST:RSEN {switch}")  # 开启远程传感（4-Wire）
        # print("4-Wire 模式已开启")

    def current_measure(self) -> float :
        meas_i = self.instrument.query('MEAS:CURR?')

        return float(meas_i)

    def voltage_measure(self) -> float :
        meas_v = self.instrument.query('MEAS:CURR?')

        return float(meas_v)

    def output_switch(self,switch : str = "OFF") -> None:
        self.instrument.write(f":OUTP {switch}")


    def force_current_set(self,current : float = 0.0):
        self.instrument.write(f":SOUR:CURR:LEV {current}")  # 设置强制输出电流值

    def force_voltage_set(self,voltage : float = 0.0):
        self.instrument.write(f":SOUR:VOLT {voltage}")

    def enter_local_mode(self):
        self.instrument.write(":TRIG:CONT RESTart")  # make SMU return to local & enter continious mode

if __name__ == "__main__" :
    """
    Take SMU 2450 as an example
    """
    smu = SMU("USB0::0x05E6::0x2450::04576516::INSTR")


    smu.force_volt_sens_cur_init(0,0.1,v_range="auto",i_range="auto",nplc=1)
    smu.force_voltage_set(0.5)
    smu.output_switch("ON")

    time.sleep(5)

    smu.force_cur_sens_volt_init(0.1,5,pIrange="auto",pVrange="auto",pNplc=1)
    smu.force_current_set(0.5)
    smu.output_switch("ON")

    time.sleep(5)

    smu.enable_4wire_mode("OFF")
    print(smu.current_measure())
    print(smu.voltage_measure())
    smu.output_switch("OFF")
