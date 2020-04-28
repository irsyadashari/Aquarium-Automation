import time
import board
import busio
import math
import adafruit_ads1x15.ads1115 as ADC
from adafruit_ads1x15.analog_in import AnalogIn


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
adc = ADC.ADS1115(i2c)

#dirty_water_voltage = 2.85

# ntu_dirty_water selain 0 - 5

def check_turbidity_values():
    #channel 0 in ADS1115 module
    channel = AnalogIn(adc, ADC.P0)
    ntu = (-26.7641 * channel.voltage) + 135.0524 
    if(ntu > 5 and ntu < 0):
        return True
    else:
        return False
