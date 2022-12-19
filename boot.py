# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
webrepl.start()
gc.collect()

#import display_climate
#import time
#display_climate.init()
#time.sleep(5)
#try:
#while True:
#  display_climate.update()
#  time.sleep(60)
#except Exception:
  # on any Exception, reboot the machine
#  import machine
#  machine.reset()

import mqtt
mqtt.main()