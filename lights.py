import mcp23017
from machine import Pin, I2C
i2c = I2C(scl=Pin(0), sda=Pin(2))
mcp = mcp23017.MCP23017(i2c, 0x20)
import uasyncio as asyncio

blink_green = asyncio.Event()

async def green_blinker():
  #await blink_green.wait()
  while True:
    if blink_green.is_set():
      print('green led on')
      mcp[8].output(1)
      await asyncio.sleep(0.5)
      print('green led off')
      mcp[8].output(0)
    await asyncio.sleep(0.5)

async def main():
  t1 = asyncio.create_task(green_blinker())
  await t1

# ways of starting things
# asyncio.run(main()) # blocks until main finishes, which is waiting for green_blinker to finish, which never does
# await asyncio.gather( ... ) # wait until all the given async finish
# await some_task # wait until the task is complete and return it's value
# Loop.run_forever() # run the loop until Loop.stop() is called - blocks
# ... _thread module?
