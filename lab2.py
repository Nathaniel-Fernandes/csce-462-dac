import time
import math

import board
import busio
import adafruit_mcp4725
import RPi.GPIO

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)

def sin_wave():
    t = 0.0
    tStep = 0.05
    while True:
        voltage = 2048*(1.0+0.5*math.sin(6.2832*t))
        dac.set_voltage(int(voltage))
        t += tStep
        time.sleep(0.0005)

def main():
    # while wait for button press:
        # ask for input: square, triangle, sin
        # ask for the 
