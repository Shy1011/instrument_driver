from instrument_drivers.base.multimeter import *

class DmmKeysight34461A(Multimeter):
    def __init__(self,device_id):
        super().__init__(device_id)


    def terminate_ongoing_measure(self):
        """
        打断仪器正在进行的操作,让仪器重新回到空闲状态
        :return:
        """
        self.instrument_write("ABORt")

    def read_buffer(self,number_of_points = 100):
        """
        P197
        read datas from the buffer
        :param number_of_points:
        :return: format list of float
        """
        assert number_of_points < 2000000, "Number of points should be greater than 0"
        if number_of_points is None:
            result = self.instrument_query(f"R?")
        else:
            result = self.instrument_query(f"R? {number_of_points}")
        return result

    def run_self_test(self)-> int:
        """
        运行仪器自检 : 返回+0表示成功，+1/+2表示失败,数字表示失败项目的个数
        :return:
        """
        result = self.instrument_query("TEST:ALL?")
        return result

    def measure_fre(self,range = 300E3):
        res = self.instrument_query(f"MEASure:FREQuency? {range}")

        return float(res)

    def read_last_measurement(self):
        """
        P244
        返回最后一次测量的值
        :return:
        """
        res = self.instrument_query(f"DATA:LAST?")

        return float(res)

    def read_data_numbers_stroed_in_buffer(self):
        """
        P244
        返回缓冲区中存储的数据点数
        :return: int : 1 2 3 100...
        """
        res = self.instrument_query(f"DATA:POINts?")

        return res

    def erase_buffer(self,numbers):
        """
        P244
        清空缓冲区
        如果numbers大于缓冲区实际的数据个数,则会报错
        :param numbers:
        :return:
        """
        self.instrument_write(f"DATA:REMove? {numbers}")

    def enable_display(self,flag = 1):
        """
        Turn on/off the screen display of the instrument.
        仪器不显示时,会让测量变得更快
        :param flag:
        :return:
        """
        self.instrument_write(f"DISPlay {flag}")

    def display_text_on_screen(self,text : str = "Hello"):
        """
        Display text on the screen of the instrument.
        :param text:
        :return:
        """
        dmm.instrument_write(f"DISPlay:TEXT '{text}'")

    def clear_text_on_screen(self):
        """
        Clear the text on the screen of the instrument.
        :return:
        """
        dmm.instrument_write("DISPlay:TEXT:CLEar")

    def enter_local_mode(self):
        """
        Enter the local mode of the instrument.
        :return:
        """
        self.instrument_write(f"SYSTem:LOCal")

    def read_internal_temperature(self):
        """
        Read the internal temperature of the instrument.
        :return:
        """
        dmm.instrument_query("SYST:TEMP?")

    def consult_run_time(self):
        dmm.instrument_query("SYST:UPT?")


    def set_trigger_source(self,source):
        """
        Set the trigger source of the instrument.
        :param source:  BUS/Single
        :return:
        """
        assert source in ["IMMediate","EXTernal","BUS"], "Invalid trigger source"
        dmm.instrument_write("TRIGger:SOURce EXTernal")

    def set_trigger_slope(self,slope):
        """
        Set the trigger slope of the instrument.
        :param slope: Positive/Negative/Either
        :return:
        """
        assert slope in ["POSitive","NEGative"], "Invalid trigger slope"
        dmm.instrument_write(f"TRIGger:SLOPe {slope}")

    def set_each_sample_times(self,times):
        """
        Each trigger how many results will be stored in the buffer.
        :param times:
        :return:
        """
        dmm.instrument_write(f"SAMP:COUN {times}")

    def read_trigger_data(self) -> list :
        """
        Read the trigger data of the instrument.
        :return:
        """
        buffer = dmm.instrument_query(f"SAMP:COUN READ?")

        return buffer

    def beep(self):
        """
        Beep the instrument.
        :return:
        """
        self.instrument_write(f"SYSTem:BEEPer")



if __name__ == "__main__":
    dmm = DmmKeysight34461A("USB0::0x2A8D::0x1301::MY60099215::INSTR")

    print(dmm.measure_dc_voltage())
    print(dmm.measure_dc_current())
    print(dmm.measure_fre())