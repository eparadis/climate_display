from umqtt.simple import MQTTClient
from lcd import puts, set_pos
import ubinascii
import machine
import time
import display_climate
import gc

# Default MQTT server to connect to
SERVER = "192.168.0.69"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

temp_tn = b"sensors/greenhouse/temperature"
rh_tn = b"sensors/greenhouse/humidity/relative"
light_tn = b"sensors/greenhouse/light"
vpd_tn = b"sensors/greenhouse/vapor_pressure_difference"
store = { temp_tn: 0,
  rh_tn: 0,
  light_tn: 0,
  vpd_tn: 0
}
new_data = False
current_line = 0

def sub_cb(topic, msg):
  global new_data, store
  if topic not in store:
    print("unexpected subscription message from topic '%s'" % (topic))
  else:
    store[topic] = float(msg.decode())
    print((topic, store[topic]))
    new_data = True

def puts_scroll(msg):
  global current_line
  set_pos(0,current_line)
  puts(msg)
  if current_line == 0:
    current_line = 1
  else:
    current_line = 0

def reset():
  puts_scroll("reseting in 3s...")
  time.sleep(3)
  import machine
  machine.reset()

def main():
  global new_data, store
  
  puts_scroll("Starting LCD...")
  display_climate.init()

  try:
    puts_scroll("Starting MQTT...")
    c = MQTTClient(CLIENT_ID, SERVER)
    c.set_callback(sub_cb)
    puts_scroll("Connecting...")
    c.connect()
    puts_scroll("%s OK" % (SERVER,))
    for topic in store.keys():
      puts_scroll("Sub'ing:%s" % (topic[-24:-16].decode(),))
      puts_scroll("'%s'" % (topic[-16:].decode())) # only show last 16 chars bc the LCD is small
      c.subscribe(topic)
      puts_scroll("..sub'd.")
      time.sleep_ms(300)
    puts_scroll("Init complete")
  except Exception as exc:
    puts_scroll(repr(exc))
    reset()

  try:
    while 1:
      # c.wait_msg() # blocking
      c.check_msg() # non-blocking
      if new_data:
        display_climate.update_display(store[temp_tn], store[rh_tn], store[light_tn], store[vpd_tn])
        new_data = False
      gc.collect()
      time.sleep_ms(500)
  except Exception as exc:
    puts_scroll(repr(exc))
    time.sleep(3)
  finally:
    reset()
