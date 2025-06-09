from instrument_drivers.base.Multimeter import *

class DmmKeysight34461A(Multimeter):
    def __init__(self,device_id):
        super().__init__(device_id)

if __name__ == "__main__":
    dmm = DmmKeysight34461A("USB0::0x2A8D::0x1301::MY60099169::INSTR")

    print(dmm.dc_voltage_measure())
    print(dmm.dc_current_measure())
    print(dmm.fre_measure())