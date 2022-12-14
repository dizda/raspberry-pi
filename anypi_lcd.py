#!/usr/bin/env python
#
#  ******************************************************************************
#  * THIS SOFTWARE IS PROVIDED IN AN "AS IS" CONDITION. NO WARRANTY AND SUPPORT *
#  * IS APPLICABLE TO THIS SOFTWARE IN ANY FORM. ANDREW WHITT SHALL NOT,        *
#  * IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL OR CONSEQUENTIAL   *
#  * DAMAGES, FOR ANY REASON WHATSOEVER.                                        *
#  ******************************************************************************
#
# Demo Program using LCM1602-14 3v3 LCD Module I2C Driver
#
# Author: Andrew Whitt
#
# Last Revised: March 2021
#

from LCM1602_3v3_I2C_DRIVER import *
from gpiozero import CPUTemperature
import subprocess
import time

cpu = CPUTemperature()
device_addr = 0x3E
max_devices = 0

def lcdSetup():
    print('Setting up LCD Module\n')
    lcdDisplay.lcdCommand(FUNCTION_SET    | FS_2_LINE)
    lcdDisplay.lcdCommand(ENTRY_MODE_SET  | EM_LEFT_TO_RIGHT | EM_DISPLAY_SHIFT_DISABLE)
    lcdDisplay.lcdCommand(DISPLAY_CONTROL | DC_DISPLAY_ON | DC_CURSOR_ON | DC_BLINK_OFF)
    lcdDisplay.positionCursor(0,0)

def adb_count():
    list_files = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE)
    list_files = list_files.stdout.decode('utf-8').split('\n')
    list_files = list(filter(None, list_files))
    total = len(list_files) - 1

    global max_devices

    if total > max_devices:
        max_devices = total

    return total

def job():
    lcdDisplay.positionCursor(0,0) # second line
    lcdDisplay.displayString(f'{adb_count()}/{max_devices} devices')
    lcdDisplay.positionCursor(1,0) # second line
    lcdDisplay.displayString(f'Temp: {cpu.temperature:.1f}C')

def main():
    try:
        lcdSetup()
        print('Displaying text...\n')

        while (True):
            job()
            time.sleep(3)


    except Exception as reason:
        print('Terminated abnormally,', reason, '\n')

if __name__ == "__main__":
    print('LCM1602A-14 3V3 1602 Serial Character LCD I2C Demo\n')
    lcdDisplay = LCM1602_3V3_LCD_I2C(device_addr)
    main()
    print('Program end.')
