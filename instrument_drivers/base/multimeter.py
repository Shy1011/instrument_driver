import time
from instrument_drivers.base.device import  *
import instrument_drivers
"""
This is a base class for multimeter instruments.

Develop a generic function for Multimeter
"""
class Multimeter(Instrument):
    def __init__(self, pInstruID):
        super().__init__(pInstruID)
        """ Voltage """
        self._last_voltage_range = None  # 缓存上一次的 range
        self._last_voltage_resolution = None  # 缓存上一次的 resolution

        self._last_current_range = None
        self._last_current_resolution = None

    def validate_nplc(self, nplc):
        # 判断当前对象是否为 Keithley6500 型号
        if isinstance(self, instrument_drivers.dmm_keithley_6500):
            # Keithley6500 支持 0.0005 到 12 之间的任意值
            return 0.0005 <= nplc <= 12
        else:
            # 其他型号仅支持特定离散值
            return nplc in {0.02, 0.2, 1, 10, 100}

    def dc_voltage_measure(self, range="10", resolution="0.0001") -> float:
        """
        测量直流电压（自动跳过重复参数配置）
        Args:
            range: 量程（可选 "0.1", "1", "10", "100", "1000", "AUTO"）
            resolution: 分辨率（可选 "0.001", "0.0001", "0.00001", "AUTO"）
        Returns:
            测量结果（浮点数）
        """
        # 参数验证
        assert range in {"0.1", "1", "10", "100", "1000", "AUTO"}, "Invalid range"
        assert resolution in {"0.001", "0.0001", "0.00001", "AUTO"}, "Invalid resolution"

        # 检查参数是否变化
        if range == self._last_voltage_range and resolution == self._last_voltage_resolution:
            # 参数未变化，直接测量
            res = self.instrument.query("MEASure:VOLTage:DC?")
        else:
            # 参数变化，更新配置并测量
            if range == "AUTO" and resolution == "AUTO":
                res = self.instrument.query("MEASure:VOLTage:DC?")
            else:
                res = self.instrument.query(f"MEASure:VOLTage:DC? {range},{resolution}")

            # 更新缓存
            self._last_voltage_range = range
            self._last_voltage_resolution = resolution

        return float(res)

    def dc_current_measure(self, range="3", resolution="0.0001") -> float:
        """
        测量直流电流（自动跳过重复参数配置）

        Args:
            range: 电流量程（可选 "0.1", "1", "3", "10", "100", "1000", "AUTO"）
            resolution: 分辨率（可选 "0.001", "0.0001", "0.00001", "AUTO"）

        Returns:
            测量结果（浮点数）
        """
        # 参数验证
        assert range in {"0.1", "1", "3", "10", "100", "1000", "AUTO"}, "请选择正确的电流量程"
        assert resolution in {"0.001", "0.0001", "0.00001", "AUTO"}, "请选择正确的分辨率"

        # 检查参数是否变化
        if range == self._last_current_range and resolution == self._last_current_resolution:
            # 参数未变化，直接测量
            res = self.instrument.query("MEASure:CURRent:DC?")
        else:
            # 参数有变化，更新配置
            if range == "AUTO" and resolution == "AUTO":
                res = self.instrument.query("MEASure:CURRent:DC?")
            else:
                res = self.instrument.query(f"MEASure:CURRent:DC? {range},{resolution}")

            # 更新缓存
            self._last_current_range = range
            self._last_current_resolution = resolution

        return float(res)

    def fre_measure(self):
        res = self.instrument.query(f"MEASure:FREQuency?")

        return float(res)

    def result_query(self):
        """
        查询测量结果
        :return: 测量结果（浮点数）
        you can set your instruments mannually then use this fuction to get query result..
        This function will not change any setting you have already made in your instrument.
        """
        res = self.instrument.query("read?")
        return float(res)

    def buzzer_ring(self,times):
        """
        Makes buzzer beep once.
        :return: none
        """
        for i  in range (times) :
            self.instrument.write("SYST:BEEP:IMM")
            time.sleep(0.5)



if __name__ == "__main__":
    dmm = Multimeter("USB0::0x05E6::0x6500::04644817::INSTR")

    print(dmm.dc_voltage_measure("AUTO","AUTO"))
    print(dmm.dc_current_measure("AUTO","AUTO"))
    print(dmm.fre_measure())
