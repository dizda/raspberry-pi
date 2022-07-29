#!/usr/bin/env python
#
#  ******************************************************************************
#  * THIS SOFTWARE IS PROVIDED IN AN "AS IS" CONDITION. NO WARRANTY AND SUPPORT *
#  * IS APPLICABLE TO THIS SOFTWARE IN ANY FORM. ANDREW WHITT SHALL NOT,        *
#  * IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL OR CONSEQUENTIAL   *
#  * DAMAGES, FOR ANY REASON WHATSOEVER.                                        *
#  ******************************************************************************
#
# LCM1602-14 3v3 I2C Serial Character LCD Module Driver
#
# Author: Andrew Whitt
#
# Last Revised: March 2021
#

import time
import smbus

# Instruction set

CLEAR_DISPLAY            = 0x01 # D0:1 Write spaces (0x20) to all DDRAM addresses
                                # Postion cursor to left edge of 1st line
                                # Set DDRAM Address Counter to Increment (Writing Left to Right)

RETURN_HOME              = 0x02 # D1:1 Return cursor to left edge of 1st line
                                # If shifted, return display to original status

ENTRY_MODE_SET           = 0x04 # D2:1 Set the moving direction of cursor and display (if shift enabled)
EM_LEFT_TO_RIGHT         = 0x02 # D1:1 (I/D) Cursor moves right and Increment DDRAM Address Counter
EM_RIGHT_TO_LEFT         = 0x00 # D1:0 (I/D) Cursor moves left and Decrement DDRAM Address Counter
EM_DISPLAY_SHIFT_ENABLE  = 0x01 # D0:1 (SH) Enable shift of display (direction determined by I/D
EM_DISPLAY_SHIFT_DISABLE = 0x00 # D0:0 (SH) Disable shift of display

DISPLAY_CONTROL          = 0x08 # D3:1 Turn On or Off Control Display, Cursor & Blink
DC_DISPLAY_ON            = 0x04 # D2:1 Turn On Display
DC_DISPLAY_OFF           = 0x00 # D2:0 Turn Off Display
DC_CURSOR_ON             = 0x02 # D1:1 Turn On Cursor
DC_CURSOR_OFF            = 0x00 # D1:0 Turn Off Cursor
DC_BLINK_ON              = 0x01 # D0:1 Turn Blink On
DC_BLINK_OFF             = 0x00 # D0:0 Turn Blink Off

SHIFT_CURSOR_DISPLAY     = 0x10 # D4:1 Shift Cursor or Display
SH_DISPLAY_RIGHT         = 0x0C # D3:1 D2:1 Shift Display Right
SH_DISPLAY_LEFT          = 0x08 # D3:1 D2:0 Shift Display Left
SH_CURSOR_RIGHT          = 0x04 # D3:0 D2:1 Shift Right and Increment DDRAM Adress Counter
SH_CURSOR_LEFT           = 0x00 # D3:0 D2:0 Shift Right and Decrement DDRAM Adress Counter

FUNCTION_SET             = 0x20 # D5:1 Line Number and Font Type
FS_2_LINE                = 0x08 # D3:1 2-Line Display Mode
FS_1_LINE                = 0x00 # D3:0 1-Line Display Mode
FS_5x11_DOTS             = 0x04 # D2:1 5x11 Dots Format
FS_5x8_DOTS              = 0x00 # D2:0 5x8 Dots Format

# local constants

_DISPLAY_LOGS = True

_i2cDev = smbus.SMBus(1)

_COLUMNS = 16
_ROWS    = 2

_CONTROL_COMMAND = 0X80  # Control Byte of Command Word
                         # Co:1 (Bit 7) Control Byte follows next Byte
                         # RS:0 (Bit 6) Next Byte is COMMAND

_CONTROL_DATA    = 0XC0  # Control Byte followed by Data Byte
                         # Co:1 (Bit 7) Control Byte follows next Byte
                         # RS:1 (Bit 6) Next Byte is DATA

_ROW_1 = 0x80  # DDRAM Address (D7:1) In 2-Line Mode, 1st Row Address Counter starts at 0x00
_ROW_2 = 0xC0  # DDRAM Address (D7:1) In 1-Line Mode, 2nd Row Address Counter starts at 0x40


class LCM1602_3V3_LCD_I2C:

    def __init__(self, lcd_address):

        if _DISPLAY_LOGS == True : print('*** Instantiating %s\n' % (type(self)))

        self.currentColumn  = 0
        self.currentRow     = 0
        self.lcdAddress     = lcd_address

        if _DISPLAY_LOGS == True : print('*** Initializing LCM1602A LCD Module\n')

        try:
        
            _i2cDev.read_byte(self.lcdAddress)

            if _DISPLAY_LOGS == True : print('*** Device found at address : %X' % (self.lcdAddress), '\n')

            self.lcdCommand(CLEAR_DISPLAY)
        
            if _DISPLAY_LOGS == True : print('*** Initialization Complete\n')

        except Exception as reason:

            print('*** Initialization Failed,', self.lcdAddress, '-', reason)

            raise SystemExit


    def lcdCommand(self, instruction):

        if _DISPLAY_LOGS == True : print('*** Sending LCD Instruction : %X' % (instruction), '\n')

        try:
        
            _i2cDev.write_byte_data(self.lcdAddress, _CONTROL_COMMAND, instruction)

            time.sleep(.01)

        except Exception as reason:

            print('!!! LCD command failed,', reason, '\n')

            raise SystemExit


    def positionCursor(self, newRow, newColumn):

        if _DISPLAY_LOGS == True : print('*** Positioning Cursor to row:%d column:%d' % (newRow, newColumn),'\n')

        try:

            column = newColumn % _COLUMNS
            row = newRow % _ROWS

            if row == 0:

                newPosition = _ROW_1 | column

            else:

                newPosition = _ROW_2 | column

            self.currentRow = row
            self.currentColumn = column

            self.lcdCommand(newPosition)

        except Exception as reason:

            print('!!! Failed to position cursor,', reason, '\n')

            raise SystemExit


    def displayString(self, string):

        if _DISPLAY_LOGS == True : print('*** Displaying string: %s' % (string), '\n')

        try:

            for i in range(len(string)):

                if _DISPLAY_LOGS == True :
                    
                    print('writing string[%d]:%X (%s) to row:%d, column:%d\n' % (i, ord(string[i]), string[i], self.currentRow, self.currentColumn))

                _i2cDev.write_byte_data(self.lcdAddress, _CONTROL_DATA, ord(string[i]))
            
                time.sleep(.001)

                self.currentColumn = self.currentColumn + 1
            
                if self.currentColumn >= _COLUMNS:
                
                    if self.currentRow == 0 : self.positionCursor(1,0)
                    
                    elif self.currentRow == 1 : self.positionCursor(0,0) 
                    
        except Exception as reason:

            print('!!! Failed to display string,', reason, '\n')

            raise SystemExit