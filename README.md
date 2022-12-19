# Greenhouse climate display

This project is a small IoT device that display the current climate in my greenhouse.

The hardware is an ESP8266 running MicroPython with an Adafruit LCD backpack connected to the two free pins on the ESP01.

Originally, the device in the greenhouse that actually measures the temperature/humidity/etc provided a simple REST API endpoint that this code used to get a JSON blob of the latest data. It now uses MQTT subscriptions to get its data. I'm not sure that's actually better in a system with only three parts, but it should pay off when I have additional sensor data streams.

# Files

`boot.py` is run at startup and kicks everything off

`mqtt.py` subscribes to the MQTT broker and tells the LCD to update when new data arrives.

`display_climate.py` contains the code to format the data and put it on the LCD. It also has the old JSON code.

`lcd.py` is a very small and rough reimplimentation of the ubiquitous Hitachi character display protocol connected in 4-bit mode via an MCP23008 I2C IO expander. It uses the `micropython-mcp230xx` library [available here](https://github.com/ShrimpingIt/micropython-mcp230xx).


