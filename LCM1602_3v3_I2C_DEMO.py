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

_LCM1602_I2C_ADDRESS = 0x3E


def lcdSetup():

    print('Setting up LCD Module\n')
    
    lcdDisplay.lcdCommand( FUNCTION_SET    | FS_2_LINE )
    lcdDisplay.lcdCommand( ENTRY_MODE_SET  | EM_LEFT_TO_RIGHT | EM_DISPLAY_SHIFT_DISABLE )
    lcdDisplay.lcdCommand( DISPLAY_CONTROL | DC_DISPLAY_ON | DC_CURSOR_ON | DC_BLINK_OFF )
    lcdDisplay.positionCursor(0,0)


def main():
    
    print('main()\n')

    try:
        
        lcdSetup()
        
        print('Displaying text...\n')

        lcdDisplay.displayString('Line One________________Line Two')

    except Exception as reason:

        print('Terminated abnormally,', reason, '\n')

if __name__ == "__main__":
    
    print('LCM1602A-14 3V3 1602 Serial Character LCD I2C Demo\n')

    lcdDisplay = LCM1602_3V3_LCD_I2C(_LCM1602_I2C_ADDRESS)

    main()
    
    print('program end')
