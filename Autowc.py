#script
from AquariumAutomation import JSNDistance
import RPi.GPIO as GPIO
import time
import datetime
from AquariumAutomation import SENTurbidity

#Set GPIO number mode BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#HIGH = MENYALA
pompa_utama = 17
pengisap = 27
pengisi = 22
lampu = 23

GPIO.setup(pompa_utama, GPIO.OUT) #pompa utama
GPIO.setup(pengisap, GPIO.OUT) #pompa pengisap
GPIO.setup(pengisi, GPIO.OUT) #pompa pengisi
GPIO.setup(lampu, GPIO.OUT) #Lampu 


#Pin untuk sensor ultrasonic water lvl akuarium
GPIO_TRIGGER_MAIN = 15
GPIO_ECHO_MAIN = 14

#Pin untuk sensor ultrasonic water lvl tanki air cadangan
GPIO_TRIGGER_SECONDARY = 25
GPIO_ECHO_SECONDARY = 24

#inisiasi mode pin untuk sensor ultrasonic
GPIO.setup(GPIO_TRIGGER_MAIN, GPIO.OUT)  # Trigger main
GPIO.setup(GPIO_TRIGGER_SECONDARY, GPIO.OUT)  # Trigger secondary
GPIO.setup(GPIO_ECHO_MAIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Echo Main
GPIO.setup(GPIO_ECHO_SECONDARY, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Echo Secondary

GPIO.output(GPIO_TRIGGER_MAIN, False)
GPIO.output(GPIO_TRIGGER_SECONDARY, False)




day_scheduled = "Monday" 

def detect_water_change():
    now = datetime.datetime.now()
    today = (now.strftime("%A"))
    
    if(today == day_scheduled):
        print("Eksekusi pergantian air metode jadwal")
        start_water_changing()
#    elif (SENTurbidity.check_turbidity_values == True):
#        print("Eksekusi pergantian air metode kekeruhan")
#        start_water_changing()
#            
    else:
        print("Air aman")
    

def start_water_changing():
    while isWaterChangeCompleted == False:
        time.sleep(2)
        if(isTankDrained == False):
            drain_half_tank()
        else :
            fill_full_tank()
            if(isWaterChangeCompleted == True):
                print("Water Change completed")
                break
      
    
#Tinggi Sensor jika tank Kosong
mainTankDistance = 70 #calibrate this
secondTankDistance = 65 #calibrate this
    
maxWater = JSNDistance.measureTank(GPIO_TRIGGER_MAIN,GPIO_ECHO_MAIN,mainTankDistance) #mengambil nilai ketinggian 
waterVolumetoChange = float(maxWater) / 15 # mengganti 1/15 volume air di dalam tank untuk testing
volumeAfterDrain =  float(maxWater) - float(waterVolumetoChange)
isTankDrained = False
isWaterChangeCompleted = False

def drain_half_tank():
#    half = maxWater/2 #kode asli
    if (float(JSNDistance.measureTank(GPIO_TRIGGER_MAIN,GPIO_ECHO_MAIN,mainTankDistance)) > float(volumeAfterDrain)):
        GPIO.output(pengisap, GPIO.LOW) #Nyalakan pompa pengisap
        time.sleep(4)
        print("penyedotan sedang berlangsung...")    
        print("Target volume air :")
        print(volumeAfterDrain)
        print("Ketinggian Air : ")
        print(JSNDistance.measureTank(GPIO_TRIGGER_MAIN,GPIO_ECHO_MAIN,mainTankDistance))
        print("\n\n")
    else :
        GPIO.output(pengisap, GPIO.HIGH) #Matikan pompa pengisap
        globals()['isTankDrained'] = True
        print("penyedotan telah selesai!\n\n")
        print("\n\n")
        time.sleep(1)
        
def fill_full_tank():
    if(float(JSNDistance.measureTank(GPIO_TRIGGER_MAIN,GPIO_ECHO_MAIN,mainTankDistance)) < float(maxWater)):
        GPIO.output(pengisi, GPIO.LOW) #Nyalakan pompa pengisi
        time.sleep(2)
        print("pengisian sedang berlangsung...\n")
        print("Ketinggian Air : ")
        print(JSNDistance.measureTank(GPIO_TRIGGER_MAIN,GPIO_ECHO_MAIN,mainTankDistance))
        print(" Target volume air :")
        print(maxWater)
        print("\n\n")
    else :
        GPIO.output(pengisi, GPIO.HIGH) #Matikan pompa pengisi
        print("mematikan pompa pengisi...")
        globals()['isWaterChangeCompleted'] = True  
        
detect_water_change()