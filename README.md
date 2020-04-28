# Aquarium-Automation
This is a library to retrieve data from lists of sensors with python on a raspberry pi.

List of sensors :

1. DS18B20 with 1 wire bus Architecture (temperature sensor)
2. JSN-SRT04 (ultrasonic sensor)
3. ACS 712 5A current sensor (with ADC converter ADS1115)
4. SEN-0189 turbidity sensor (with ADC converter ADS1115)

Autowc.py is a script where you can do an automatic water change by controlling your water pump with relay based on ultrasonic sensors readings to detect how many water you would like to change
