import time
from instrument_drivers.base.Device import  *
"""
This is the base class for the Keithley SourceMeter.

Develop a generic function for SMU
"""

class Smu(Instrument):
    def __init__(self, pInstruID):
        super().__init__(pInstruID)
        self.v_range = {0.2,2,7,10,20,100,"auto"}
        self.i_range = {0.00001,0.0001,0.001,0.01,0.1,1, "auto"}

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
        assert v_range in self.v_range,"Paramemter v_range illegal"
        assert i_range in self.i_range, "Paramemter i_range illegal"

        # 电压源配置
        self.instrument.write(":SOUR:FUNC VOLT")


        # 量程设置（三目运算符简化）
        v_range_cmd = ":SOUR:VOLT:RANG:AUTO ON" if isinstance(v_range, str) else f":SOUR:VOLT:RANG {v_range}"
        i_range_cmd = ":SENS:CURR:RANG:AUTO ON" if isinstance(i_range, str) else f":SENS:CURR:RANG {i_range}"



        self.instrument.write(v_range_cmd)
        self.instrument.write(":SENS:FUNC 'CURR'")
        self.instrument.write(i_range_cmd)
        self.instrument.write(f":SENS:CURR:NPLC {nplc}")
        self.instrument.write(f":SOUR:VOLT {v_out}")
        self.instrument.write(f":SOUR:VOLT:ILIM {i_limit}")



    def force_cur_sens_volt_init(
            self,
            i_out: float | str = 0.1,
            v_limit: float | str = 5,
            i_range: float | str = "auto",
            v_range: float | str = "auto",
            nplc: float | str = 1,
    ) -> None:
        """
        配置 SMU（源测量单元）为 ​**强制电流模式（Force Current）​**，并设置 ​**电压测量（Sense Voltage）​**。

        Args:
            i_out (float | str): 强制输出的电流值（单位：A），例如 `0.1` 或 `"100e-3"`。
            v_limit (float | str): 强制电流模式下的电压限制（单位：V），例如 `10.0` 或 `"10"`。
            i_range (float | str): 电流量程（数值或 `"AUTO"`），例如 `1.0` 或 `"AUTO"`。
            v_range (float | str): 电压测量量程（数值或 `"AUTO"`），例如 `10.0` 或 `"AUTO"`。
            nplc (float | str): 电压测量的积分时间（NPLC），例如 `1` 或 `"10"`。

        Returns:
            None
        """
        assert v_range in self.v_range,"Paramemter v_range illegal"
        assert i_range in self.i_range, "Paramemter i_range illegal"

        # --- 源代码配置 ---
        self.instrument.write(":SOUR:FUNC CURR")  # 设置 SMU 源模式为电流输出


        # 设置电流量程（自动或固定值）
        if isinstance(i_range, str) and i_range.upper() == "AUTO":
            self.instrument.write(":SOUR:CURR:RANG:AUTO ON")
        else:
            self.instrument.write(f":SOUR:CURR:RANG {i_range}")

        # --- 测量配置 ---
        self.instrument.write(":SENS:FUNC 'VOLT'")  # 设置 SMU 测量模式为电压

        # 设置电压量程（自动或固定值）
        if isinstance(v_range, str) and v_range.upper() == "AUTO":
            self.instrument.write(":SENS:VOLT:RANG:AUTO ON")
        else:
            self.instrument.write(f":SENS:VOLT:RANG {v_range}")

        self.instrument.write(f":SENS:VOLT:NPLC {nplc}")  # 设置电压测量的积分时间（NPLC）
        self.instrument.write(f":SOUR:CURR:LEV {i_out}")  # 设置强制输出电流值
        self.instrument.write(f":SOUR:CURR:VLIM {v_limit}")  # 设置电流模式下的电压限制

    def enable_4wire_mode(self,switch : bool = False) -> None:
        """启用 4-Wire 测量模式（不改变其他配置）"""
        if switch:
            self.instrument.write(f":SYST:RSEN ON")  # 开启远程传感（4-Wire）
        else :
            self.instrument.write(f":SYST:RSEN OFF")  # （2-Wire）


    def current_measure(self) -> float :
        meas_i = self.instrument.query('MEAS:CURR?')

        return float(meas_i)

    def voltage_measure(self) -> float :
        meas_v = self.instrument.query('MEAS:CURR?')

        return float(meas_v)

    def enable_output(self, switch : bool = False) -> None:
        if switch:
            self.instrument.write(f":OUTP ON")
        else:
            self.instrument.write(f":OUTP OFF")


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
    smu = Smu("USB0::0x05E6::0x2460::04576516::INSTR")


    smu.force_volt_sens_cur_init(0,0.1,v_range="auto",i_range="auto",nplc=1)
    smu.force_voltage_set(0.5)
    smu.enable_output(True)

    time.sleep(5)

    smu.force_cur_sens_volt_init(0.1, 5, i_range="auto", v_range="auto", nplc=1)
    smu.force_current_set(0.5)
    smu.enable_output(True)

    time.sleep(5)

    smu.enable_4wire_mode(False)
    print(smu.current_measure())
    print(smu.voltage_measure())
    smu.enable_output(False)
