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

#calibrate this according to the sensors. In this case, I use the 5A version
sensitivity = 185 # mv/A for ACS712 5A version, 100 mV/A for 20A version, and 66 mv/A for 30A version

#jika tak ada arus, tegangan harusnya 0
offsetVoltage = 0.5


def get_current_values(channel_num):

    chan = ADC.P1 
    if (channel_num == 1):
        chan = ADC.P1

    if(channel_num == 2):
        chan = ADC.P2
        
    channel = AnalogIn(adc,chan)
    current = (channel.voltage - offsetVoltage) / sensitivity
    return current

def get_battery_estimated_life(battery_power, current_flow, battery_deficiency):
    usage_time = battery_power/current_flow
    deficiency = usage_time*(battery_deficiency/100)
    estimated_usage_time = usage_time - deficiency
    minutes = (estimated_usage_time % 1) * 60
    hour = estimated_usage_time - (estimated_usage_time % 1)
#
#    print("Hour : ")
#    print(str("%.0f" % hour))
#    print("Minutes : ")
#    print(str("%.0f" % minutes))
    return hour, minutes


   
