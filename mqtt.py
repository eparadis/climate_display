from umqtt.simple import MQTTClient
import ubinascii
import machine
import time

# Default MQTT server to connect to
SERVER = "192.168.0.69"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

store = { b"sensors/greenhouse/temperature": 0,
  b"sensors/greenhouse/humidity/relative": 0,
  b"sensors/greenhouse/light": 0,
  b"sensors/greenhouse/vapor_pressure_difference": 0
}

def sub_cb(topic, msg):
    if topic not in store:
        print("unexpected subscription message from topic '%s'" % (topic))
    else:
        store[topic] = msg
        print((topic, msg))

def main():
    c = MQTTClient(CLIENT_ID, SERVER)
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    print("Connected to %s" % (SERVER,))
    for topic in store.keys():
        print("Subscribing to topic '%s'" % (topic))
        c.subscribe(topic)
        print("...subscribed. Throttling for 1 second")
        time.sleep(1)
    print("Initialization complete")

    try:
        while 1:
            # micropython.mem_info()
            c.wait_msg()
    finally:
        c.disconnect()
