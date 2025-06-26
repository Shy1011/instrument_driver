"""
此模块需要配合Bridge板使用,使用前请先引入beidge板驱动
"""

def set_relay_unit(pHidBridge, relayNum):
    """
    This function used to set the relay unit
    :param pHidBridge: hid object
    :param relayNum: which relay need to be set 0 -
    """
    relayNum = relayNum + 1
    if 0 < relayNum <= 8:
        ch32_i2c_write(pHidBridge, 0xE0, 0x00, [0x03, (0x01 << relayNum - 1) ^ 0xFF])  # i2c slave_addr is 0xE0
        # print(bin(0x01 << relyNum))
    elif relayNum == 9:
        ch32_i2c_write(pHidBridge, 0xE0, 0x00, [0x03, 0xFF])  # i2c slave_addr is 0xE0


def set_relay_multi(pHidBridge, pPos, pStatus):
    """
    This function used to turn on multichannel relay from start to end and turn off all relay
    :param pHidBridge: hid object
    :param pPos: relay need to be turned on (list length is 8)
    :param pStatus: ON or OFF
    :return: None
    """
    if 1 <= len(pPos) <= 8:
        relay_pos = 0xFF
        if pStatus == "ON":
            for i in pPos:
                relay_pos = (0x01 << (i - 1)) ^ relay_pos
        else:
            relay_pos = 0xFF

        ch32_i2c_write(pHidBridge, 0xE0, 0x00, [0x03, relay_pos])  # i2c slave_addr is 0xE0
    else:
        print("parameter error")

