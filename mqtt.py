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

def sub_cb(topic, msg):
    global new_data, store
    if topic not in store:
        print("unexpected subscription message from topic '%s'" % (topic))
    else:
        store[topic] = float(msg.decode())
        print((topic, store[topic]))
        new_data = True

def puts_firstline(msg):
    set_pos(0,0)
    puts(msg)

def puts_secondline(msg):
    set_pos(0,1)
    puts(msg)

def main():
    global new_data, store
    
    puts_secondline("Starting LCD...")
    display_climate.init()

    puts_firstline("Starting MQTT...")
    try:
      c = MQTTClient(CLIENT_ID, SERVER)
    except Exception as exc:
        puts_secondline(repr(exc))
        puts_firstline("sleeping...")
        time.sleep(5)
        puts_secondline("reseting...")
        import machine
        machine.reset()
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    puts_secondline("%s OK" % (SERVER,))
    for topic in store.keys():
        puts_firstline("Sub'ing to:%s" % (topic[-20:-16],))
        puts_secondline("'%s'" % (topic[-16:])) # only show last 16 chars bc the LCD is small
        c.subscribe(topic)
        puts_secondline("..sub'd. wait 1s")
        time.sleep(1)
    puts_firstline("Init complete")

    try:
        while 1:
            # micropython.mem_info()
            # c.wait_msg()
            c.check_msg()
            if new_data:
                display_climate.update_display(store[temp_tn], store[rh_tn], store[light_tn], store[vpd_tn])
                new_data = False
            gc.collect()
            time.sleep_ms(500)
    except Exception as exc:
        puts_firstline(repr(exc))
    finally:
        puts_secondline("disconnecting")
        c.disconnect()
        puts_firstline("sleeping...")
        time.sleep(5)
        puts_secondline("reseting...")
        import machine
        machine.reset()
