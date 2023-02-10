import time
import math
import board
import busio
import adafruit_mcp4725
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

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
    GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    # wait for initial button press
    GPIO.wait_for_edge(40, GPIO.rising)

    while True:
        # ask for input: wave type, frequency, and output voltage
        shape = input("Would you like a 'square', 'triangle', or 'sin' wave?")
        frequency = input("What's the frequency?")
        max_vout = input("What's the max output voltage?")

        while True:
            
            if shape == "sin":
                sin_wave()
                
            # button press
            if GPIO.input(40):
                break

