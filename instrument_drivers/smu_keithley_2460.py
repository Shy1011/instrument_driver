from instrument_drivers.base.smu import *

class SmuKeithley2460(Smu):
    def __init__(self,device_id):
        super().__init__(device_id)
        self.v_range = {0.2,2,7,10,20,100,"auto"}
        self.i_range = {0.00001,0.0001,0.001,0.01,0.1,1,4,5,7, "auto"}

    def run_macro_script(self,script_name):
        """
        User Mannual P120
        You can run a macro script from the front panel or from a remote interface.
        :param script_name: the name of the macro script to be run. It should be referred in the SMU panel.
        :return:
        """
        self.instrument_write(f"SCRipt:RUN {script_name}")  # load macro script

    def set_output_off_state(self,state):
        """
        P138 User Manual

        当仪器输出为OFF状态时，选择输出的状态：NORMal, ZERO, HIMPedance, GUARd.
        NORMal: 默认用这种模式
        ZERO:
        HIMPedance: Output的继电器物理断开,其他的都不是.确保SMU不会影响待测电路. [可以听见继电器的响声]
        GUARd:
        :param state:
        :return:
        """
        assert state in ["NORMal","ZERO","HIMPedance","GUARd"] , "Parameter state illegal"

        self.instrument_write(f":OUTPut:SMODe {state}")


    def compensate_offset_ohms(self):
        """
        P152 User Manual
        热电电动势（VEMF）产生的电压偏移会显著影响电阻测量精度。为消除偏移电压的影响，可采用偏移补偿欧姆测量法
        [不同金属接触点存在温差时（如铜导线与镍合金端子），会因塞贝克效应（Seebeck effect）产生μV级寄生电压。]
        :return:
        """
        self.instrument_write("SENSe:RESistance:OCOMpensated ON")

    def select_nplc(self,mode,nplc):
        """
        P227 User Manual
        选择测量精度,可单独设置 电流 电压 电阻的测量精度.
        注意 请选择当前模式对应的测量精度.如果和当前测量的模式不匹配则此条指令不会生效
        例如 : force_volt_sens_cur_init() 选择Current的nplc 有效范围为 0.01 - 10
                force_cur_sens_volt_init() 选择voltage的nplc 有效范围为 0.01 - 10
        :param nplc: 0.01 - 10
        :param mode: VOLTage, CURRent, RESistance
        :return:
        """

        self.instrument_write(f":SENSe:{mode}:NPLCycles {nplc}")

    def select_high_capacitance_mode(self,enable:str = "OFF"):
        """
        P239 User Manual
        选择高电容模式,在为大电容负载提供源时开启此模式. 但是测量速度会变慢
        :param enable:  on/off Default is off
        :return:
        """
        self.instrument_write(f":SOURce:Voltage:HIGH:CAPacitance {enable}")


    """ BUFFER SECTION """
    """ BUFFER SECTION """
    """ BUFFER SECTION """

    def create_buffer(self,buffer_name : str,buffer_size : int,fill_mode : str):
        """
        P257 User Manual
        创建一个Buffer,用于存储测量数据.
        :param buffer_name: buffer name
        :param buffer_size: buffer size
        :param fill_mode:  Standard.Compact,Full  填充数据的准确度, Compact是6.5 digits
        :return:
        """

        self.instrument_write(f"TRACe:MAKE '{buffer_name}', {buffer_size}, {fill_mode}")

    def set_buffer_capacitance(self,buffer_name : str,capacitance : int):
        """
        P257 User Manual
        设置Buffer的数据存储数量
        :param buffer_name:
        :param capacitance:
        :return:
        """
        self.instrument_write(f"TRACe:POINts {capacitance}, '{buffer_name}'")


    def set_buffer_fill_mode(self,buffer_name : str,fill_mode : str):
        """
        P257 User Manual
        设置Buffer的填充模式
        :param buffer_name:
        :param fill_mode: CONT/ONCE  once 填满一次, CONT 填满之后,新数据从头覆盖
        :return:
        """
        self.instrument_write(f"TRACe:FILL:MODE {fill_mode}, '{buffer_name}'")


    def measure_and_store_buffer(self,buffer_name : str,mode : str) -> float:
        """
        P264
        测量一次,并将指定当前数据存入到buffer中
        :param buffer_name:
        :param mode:
        :return:  返回测量的数据
        """
        data = self.instrument_write(f":MEASure: {mode}?, '{buffer_name}'")

        return data

    def save_readings_to_usb(self,path,buffer_name : str):
        """
        P271
        :param path:
        :param buffer_name:
        :return:
        """

        pass

    def clear_buffer(self,buffer_name : str):
        """
        Clear the buffer
        :param buffer_name:
        :return:
        """
        self.instrument_write(f"TRACe:CLEar '{buffer_name}'")

    def delete_buffer(self,buffer_name : str):

        self.instrument_write(f":TRACe:DELete '{buffer_name}'")


    """ Digitial IO Settings """
    """ Digitial IO Settings """
    """ Digitial IO Settings """




if __name__ == "__main__" :
    smu = SmuKeithley2460("USB0::0x05E6::0x2460::04624797::INSTR")
    default1 = ForceVoltSenseCurConfig()  # setup for SMU1
    default2 = ForceCurSenseVoltConfig()  # setup for SMU2

    default1.v_out = 0.2

    smu.force_volt_sens_cur_init(default1)
    smu.enable_output(True)
    smu.force_cur_sens_volt_init(default2)
    smu.enable_output(True)
    smu.enter_local_mode()

