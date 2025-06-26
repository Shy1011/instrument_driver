from instrument_drivers.base.device import *

"""
This is the base class for the DAQ instruments.
继电器的驱动
"""


class Daq(Instrument):
    def __init__(self, pInstruID):
        super().__init__(pInstruID)

    def wait(self):
        """
        查询仪器中所有模块（或插卡）的等待状态，确认它们是否已完成当前操作
        如果没有完成则等待,动作完成再执行下一步
        :return:
        """
        # self.instrument_write('ROUT:OPER:OVER:ENAB ON')
        self.instrument_query('ROUT:MOD:WAIT? ALL')

    def close(self, chan, *, wait=True):
        if isinstance(chan, int):
            chn_txt = str(chan)
        else:
            chn_txt = ','.join(map(str, chan))

        cmd_str = f'ROUTe:CLOSe (@{chn_txt})'

        self.instrument_write(cmd_str)

        if wait:
            self.wait()

    def close_only(self, chan, *, wait=True):  # CLOSE:EXCLUSIVE performs an open all only on cards affected followed by close of selected channels
        self.open_all()

        if isinstance(chan, int):
            chn_txt = str(chan)
        else:
            chn_txt = ','.join(map(str, chan))
        cmd_str = f'ROUTe:CLOSe:EXCLusive (@{chn_txt})'

        self.instrument_write(cmd_str)
        if wait:
            self.wait()

    def close_all(self):
        raise Exception("Oh, no! That's too dangerous, please don't do that!")

    def open_range(self, from_chan, to_chan, *, wait=True):
        assert isinstance(from_chan, int)
        assert isinstance(to_chan, int)
        cmd_str = f'ROUTe:OPEN (@{from_chan}:{to_chan})'
        self.instrument_write(cmd_str)
        if wait:
            self.wait()

    def open(self, chan, *, wait=True):
        if isinstance(chan, int):
            chn_txt = str(chan)
        else:
            chn_txt = ','.join(map(str, chan))
        cmd_str = f'ROUTe:OPEN (@{chn_txt})'

        self.instrument_write(cmd_str)
        if wait:
            self.wait()

    def open_abus(self, abus=None, *, wait=True):
        if abus == None:
            self.instrument_write('ROUTe:OPEN:ABUS ALL')
        else:
            self.instrument_write(f'ROUTe:OPEN:ABUS {abus}')
        if wait:
            self.wait()

    def open_all(self, slot=None, *, wait=True):
        if slot == None:
            self.instrument_write('ROUTe:OPEN:ALL ALL')
        else:
            self.instrument_write(f'ROUTe:OPEN:ALL {slot}')
        if wait:
            self.wait()

    def hint(self, tips):
        init(autoreset=True)
        print(Fore.RED)
        print(Fore.RED+"!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(Fore.RED+tips)
        print(Fore.RED+"!!!!!!!!!!!!!!!!!!!!!!!!!!!")
