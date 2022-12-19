import mcp
import time
m = mcp.MCP23008(0x21, 0, 2)
m.output(7, True)  # turn on backlight

def pulse_enable():
  enable = 2
  m.output(enable, False)
  time.sleep_us(1)
  m.output(enable, True)
  time.sleep_us(1)
  m.output(enable, False)
  time.sleep_us(1)

def write8(val, char_mode=False):
  # pins (0 is N/C and 7 is the backlight)
  reset = 1
  d4 = 3
  d5 = 4
  d6 = 5
  d7 = 6
  time.sleep(0.001)
  m.output(reset, char_mode)
  m.output(d4, ((val >> 4) & 1) > 0)
  m.output(d5, ((val >> 5) & 1) > 0)
  m.output(d6, ((val >> 6) & 1) > 0)
  m.output(d7, ((val >> 7) & 1) > 0)
  pulse_enable()
  m.output(d4, (val & 1) > 0)
  m.output(d5, ((val >> 1) & 1) > 0)
  m.output(d6, ((val >> 2) & 1) > 0)
  m.output(d7, ((val >> 3) & 1) > 0)
  pulse_enable()

def clear():
  write8(0x01)
  time.sleep(0.003)

def initialize():
  # set all pins to output
  for pinNum in list(range(0,8)):
    m.setup(pinNum, mcp.OUT)
  write8(0x33)
  write8(0x32)
  write8(0x08 | 0x04 | 0x00 | 0x00) # display control
  write8(0x20 | 0x00 | 0x00 | 0x08 | 0x00) # display function set
  write8(0x04 | 0x02 | 0x00) # display mode set  
  clear()

def puts( s):
  for c in s:
    write8(ord(c), True)

def set_pos( col, row):
  write8(0x80 | col + (0x40 if row == 1 else 0x00))


