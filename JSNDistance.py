import RPi.GPIO as GPIO
import time

TRIGGER_TIME = 0.00001
MAX_TIME = 0.004  # max time waiting for response in case something is missed

#Set GPIO number mode BCM
GPIO.setmode(GPIO.BCM)

# This function measures a distance
def measureTank(triggerPin,echoPin,bottomTankDistance):
    # Pulse the trigger/echo line to initiate a measurement
    GPIO.output(triggerPin, True)
    time.sleep(TRIGGER_TIME)
    GPIO.output(triggerPin, False)

    # ensure start time is set in case of very quick return
    start = time.time()
    timeout = start + MAX_TIME

    # set line to input to check for start of echo response
    while GPIO.input(echoPin) == 0 and start <= timeout:
        start = time.time()

    if(start > timeout):
        return "out of range"

    stop = time.time()
    timeout = stop + MAX_TIME
    # Wait for end of echo response
    while GPIO.input(echoPin) == 1 and stop <= timeout:
        stop = time.time()

    if(stop <= timeout):
        elapsed = stop-start
        distance = float(elapsed * 34300)/2.0
    else:
        return "out of range"
    return str("%.2f" % (bottomTankDistance-distance))
