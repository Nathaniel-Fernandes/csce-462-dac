import time
import math
import board
import busio
import adafruit_mcp4725
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)

def sin_wave(freq: int, max_voltage: int):
    t = 0.0
    tStep = 0.05
    while True:
        voltage = int(max_voltage*math.sin(2*math.pi*freq*t))
        dac.raw_value = min(voltage, 4095)

        t += tStep
        time.sleep(0.0005) # off by 0.0005 each time

        # button press to halt
        if GPIO.input(40):
            return

def square(freq: int, max_voltage: int):
    t = 0
    tStep = 0.05
    while True:
        # set voltage high if in 1st half of cycle, low if 2nd half of cycle
        if (t % 1/freq) < 1/(2*freq):
            dac.raw_value = max_voltage
        else:
            dac.raw_value = 0

        t += tStep   
        time.sleep(0.0005)

        if GPIO.input(40):
            return

def triangle(freq: int, max_voltage: int):
    t = 0
    tStep = 0.05
    while True:
        # set voltage high if in 1st half of cycle, low if 2nd half of cycle
        if (t % 1/freq) < 1/(2*freq):
            dac.raw_value = (max_voltage / (1/(2 * freq)))*t # y = mx + b, where b=0, m=max voltage/half period
        else:
            # y = m(x - x0) + y0, where y0=0, m= -max voltage/half period
            dac.raw_value = -(max_voltage / (1/(2 * freq)))*(t - (1/(2*freq))) + max_voltage

        t += tStep   
        time.sleep(0.0005)

        if GPIO.input(40):
            return

def main():
    GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    # use interrupt to wait for button press
    GPIO.wait_for_edge(40, GPIO.rising)

    while True:
        # ask user for wave type, frequency, and output voltage
        wave_shape = input("Would you like a 'square', 'triangle', or 'sin' wave?")
        wave_freq = int(input("What's the frequency?"))
        wave_max_voltage = int(input("What's the max output voltage?"))

        if wave_shape == "sin":
            sin_wave(wave_freq, wave_max_voltage)
        
        elif wave_shape == "square":
            square(wave_freq, wave_max_voltage)
        
        elif wave_shape == "triangle":
            triangle(wave_freq, wave_max_voltage)
                
            

