from umqtt.simple import MQTTClient
import ubinascii
import machine

# Default MQTT server to connect to
SERVER = "192.168.0.69"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"sensors/greenhouse/temperature"

def sub_cb(topic, msg):
    print((topic, msg))

def main(server=SERVER):
    c = MQTTClient(CLIENT_ID, server)
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))

    try:
        while 1:
            # micropython.mem_info()
            c.wait_msg()
    finally:
        c.disconnect()
