# Greenhouse climate display

This project is a small IoT device that display the current climate in my greenhouse.

The hardware is an ESP8266 running MicroPython with an Adafruit LCD backpack connected to the two free pins on the ESP01.

Originally, the device in the greenhouse that actually measures the temperature/humidity/etc provided a simple REST API endpoint that this code used to get a JSON blob of the latest data. As I move more of my system to MQTT, I plan to have this device subscribe to topics on the MQTT broker to decouple this project from the other somewhat.

# Files

`boot.py` is run at startup and kicks everything off
`display_climate.py` contains the code to request the latest data, format it, and put it on the LCD
`lcd.py` is a very small and rough reimplimentation of the ubiquitous Hitachi character display protocol connected in 4-bit mode via an MCP23008 I2C IO expander. It uses the `micropython-mcp230xx` library [available here](https://github.com/ShrimpingIt/micropython-mcp230xx).


