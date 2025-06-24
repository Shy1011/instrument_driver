import time
from instrument_drivers.base.device import  *
from dataclasses import dataclass
"""
This is the base class for the Keithley SourceMeter.

Develop a generic function for SMU
"""

@dataclass
class ForceVoltSenseCurConfig:
    v_out: float | str = 0  # 电压源输出值（单位：V）
    i_limit: float | str = 1  # 电压源模式下的电流限值（单位：A）
    v_range: float | str = "auto"  # 电压源量程，数值为具体量程，字符串表示自动量程
    i_range: float | str = "auto"  # 电流测量量程，数值为具体量程，字符串表示自动量程
    nplc: float = 1  # 电流测量的积分时间（NPLC值）


@dataclass
class ForceCurSenseVoltConfig:
    """强制电流模式配置参数"""
    i_out: float | str = 0.1      # 强制输出的电流值（单位：A）
    v_limit: float | str = 5      # 电流模式下的电压限制（单位：V）
    i_range: float | str = "auto" # 电流量程（数值或"auto"）
    v_range: float | str = "auto" # 电压测量量程（数值或"auto"）
    nplc: float | str = 1         # 电压测量的积分时间（NPLC）


class Smu(Instrument):
    def __init__(self, pInstruID):
        super().__init__(pInstruID)
        self.v_range = {0.2,2,7,10,20,100,"auto"}
        self.i_range = {0.00001,0.0001,0.001,0.01,0.1,1, "auto"}

    def force_volt_sens_cur_init(self, config: ForceVoltSenseCurConfig) -> None:
        """
        配置设备为电压源输出、电流测量模式（Force Voltage, Sense Current）

        参数：
            config: 包含所有配置参数的数据类对象
        """
        assert config.v_range in self.v_range, "Parameter v_range illegal"
        assert config.i_range in self.i_range, "Parameter i_range illegal"

        self.instrument_write(":SOUR:FUNC VOLT")

        v_range_cmd = ":SOUR:VOLT:RANG:AUTO ON" if isinstance(config.v_range,
                                                              str) else f":SOUR:VOLT:RANG {config.v_range}"
        i_range_cmd = ":SENS:CURR:RANG:AUTO ON" if isinstance(config.i_range,
                                                              str) else f":SENS:CURR:RANG {config.i_range}"

        self.instrument_write(v_range_cmd)
        self.instrument_write(":SENS:FUNC 'CURR'")
        self.instrument_write(i_range_cmd)
        self.instrument_write(f":SENS:CURR:NPLC {config.nplc}")
        self.instrument_write(f":SOUR:VOLT {config.v_out}")
        self.instrument_write(f":SOUR:VOLT:ILIM {config.i_limit}")

    def enable_high_cap(self, switch: bool = False) -> None:
        """"
        启动高电容模式.适合容性负载
        """
        if switch:
            self.instrument_write(f':SOURce:CURRent:HIGH:CAPacitance ON')
        else:
            self.instrument_write(f':SOURce:CURRent:HIGH:CAPacitance OFF')

    def force_cur_sens_volt_init(self, config: ForceCurSenseVoltConfig) -> None:
        """
        配置设备为电流源输出、电压测量模式（Force Current, Sense Voltage）

        参数：
            config: 包含所有配置参数的数据类对象
        """
        assert config.v_range in self.v_range, "Parameter v_range illegal"
        assert config.i_range in self.i_range, "Parameter i_range illegal"

        # 电流源配置
        self.instrument_write(":SOUR:FUNC CURR")


        i_range_cmd = ":SOUR:CURR:RANG:AUTO ON" if isinstance(config.i_range,
                                                              str) else f":SOUR:CURR:RANG {config.i_range}"
        v_range_cmd = ":SENS:VOLT:RANG:AUTO ON" if isinstance(config.v_range,
                                                              str) else f":SENS:VOLT:RANG {config.v_range}"

        self.instrument_write(i_range_cmd)
        self.instrument_write(":SENS:FUNC 'VOLT'")
        self.instrument_write(v_range_cmd)
        self.instrument_write(f":SENS:VOLT:NPLC {config.nplc}")
        self.instrument_write(f":SOUR:CURR:LEV {config.i_out}")
        self.instrument_write(f":SOUR:CURR:VLIM {config.v_limit}")

    def enable_4wire_mode(self,switch : bool = False) -> None:
        """启用 4-Wire 测量模式（不改变其他配置）"""
        if switch:
            self.instrument_write(f":SYST:RSEN ON")  # 开启远程传感（4-Wire）
        else :
            self.instrument_write(f":SYST:RSEN OFF")  # （2-Wire）

    def voltage_measure_wait_stable(self,diff,interval):
        '''
        等待电压稳定，返回最后一次测量值
        :param diff: 最大允许的电压误差  任何电压都被允许
        :param interval: 采集电压的时间间隔
        :return:
        '''
        history=[]

        while 1:
            now=time.perf_counter()
            history.append((now,self.voltage_measure()))
            if history[-1][0]-history[0][0]>interval:
                meas_list=sorted([k[1] for k in history])
                if meas_list[-1]-meas_list[0]<diff:
                    break
            expire=now-interval
            history=[p for p in history if p[0]>expire]
            # print(history)

        return history[-1][1]


    def measure_current(self) -> float :
        meas_i = self.instrument_query('MEAS:CURR?')

        return float(meas_i)

    def measuere_voltage(self) -> float :
        meas_v = self.instrument_query('MEAS:VOLT?')

        return float(meas_v)

    def enable_output(self, switch : bool = False) -> None:
        if switch:
            self.instrument_write(f":OUTP ON")
        else:
            self.instrument_write(f":OUTP OFF")


    def force_current_set(self,current : float = 0.0):
        self.instrument_write(f":SOUR:CURR:LEV {current}")  # 设置强制输出电流值

    def force_voltage_set(self,voltage : float = 0.0):
        self.instrument_write(f":SOUR:VOLT {voltage}")


    """ Below  are the functions which are not used very often, but may be useful in some cases."""
    """ Below  are the functions which are not used very often, but may be useful in some cases."""
    """ Below  are the functions which are not used very often, but may be useful in some cases."""

    def enter

    def enter_local_mode(self):
        self.instrument_write(":TRIG:CONT RESTart")  # make SMU return to local & enter continious mode



if __name__ == "__main__" :
    """
    Take SMU 2450 as an example
    """
    default1 = ForceVoltSenseCurConfig()  # setup for SMU1
    default2 = ForceCurSenseVoltConfig()  # setup for SMU2

    default1.v_out = 0.2
    default2.i_out = 0.1

    smu = Smu("USB0::0x05E6::0x2460::04624797::INSTR")


    smu.force_volt_sens_cur_init(default1)
    smu.force_voltage_set(0.5)
    smu.enable_output(True)

    time.sleep(5)

    smu.force_cur_sens_volt_init(default2)
    smu.force_current_set(0.5)
    smu.enable_output(True)

    time.sleep(5)

    smu.enable_4wire_mode(False)
    print(smu.current_measure())
    print(smu.voltage_measure())
    smu.enable_output(False)
