import pyvisa
from txt import *
import time
from datetime import datetime
import pathlib

"""
This will scan all the instruments connected to the computer and save their ID's in a txt file.
"""

if __name__ == "__main__" :
    start = time.time()
    save_path = rf"files"  # will have to create a folder named "files" in the same directory as the script, and a txt file will be saved there
    pathlib.Path(save_path).mkdir(exist_ok=True)

    now = datetime.now()
    custom_format = now.strftime("%Y_%m_%d_ %H_%M_%S")

    handler_with_timestamp = TxtFileHandler(file_name="Instrument_Info", save_path=save_path, mode='a', show_content=False,
                                            save_file=True, use_timestamp=False)
    rm = pyvisa.ResourceManager()
    instruments = rm.list_resources()

    handler_with_timestamp.write_to_txt(f"\n-------------------------------------------------{custom_format}-----------------------------------------------------\n")


    for instrument in instruments:
        try :
            device = rm.open_resource(instrument)  # open instrument through instruID
            device.read_termination = "\n"
            device.timeout = 2000# set instrument timeout
            instrument_info = device.query("*IDN?")
            print(f"{instrument_info}------{instrument}")  # print instrument ID
            handler_with_timestamp.write_to_txt( f"{instrument:60}{instrument_info:60}\n")
        except Exception as e :
            print("Nothing")

    end = time.time()
    print(f"耗时: {end - start:.2f} 秒")

