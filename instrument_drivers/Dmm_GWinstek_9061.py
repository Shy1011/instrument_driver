from instrument_drivers.parent_classes.Multimeter import *

class Dmm_GWINSTEK_9061(MULTIMEMTER):
    def __init__(self,device_id):
        super().__init__(device_id)
        self.instrument.write("SENS:AVER:STAT OFF")  # cancel the digital filter






if __name__ == "__main__":
    dmm = Dmm_GWINSTEK_9061("USB0::0x2184::0x0059::GEW912502::INSTR")

    print(dmm.dc_voltage_measure())
    print(dmm.dc_current_measure())
    print(dmm.fre_measure())
