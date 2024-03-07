#Team The Futurists
#Battery Management System 
#This code is for Taking Sensor input and sending on the ThingSpeak Cloud
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import urllib.request


led=4       #led on
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,True)

#relay and their GPIO pin config
relay_1=21
relay_2=20
relay_3=12

#ir pin config
ir=22
GPIO.setup(ir,GPIO.IN)


#temp and humidity pin config
pin_1=2
pin_2=3

#gas sensor GPIO pin config
gas=10


def sensors_code():

    humidity,temperature =Adafruit_DHT.read_retry(Adafruit_DHT.DHT11,pin_1)     #for sensor 1 T&H

    humidity2,temperature2 =Adafruit_DHT.read_retry(Adafruit_DHT.DHT11,pin_2)   #for sensor 2 T&H

    if humidity is not None and temperature is not None:    #for sensor 1 T&H
        print('Temp={0:0.1f}*C' 'Humidity={1:0.1f}%'.format(temperature,humidity))
    else:
        print('Failed to get readings. Try again')

    hm=(humidity+humidity2)/2


    flag_1=0
    if temperature > 30:           #relay 1 for battery heat reducing i.e on the fan/cooling device
        GPIO.output(relay_1,True)
        flag_1=1
    else:
        GPIO.output(relay_1,False)

    time.sleep(2)

#-------------------------------------------------------------------------------------------#
    
    if humidity is not None and temperature is not None:    #for sensor 2 T&H
        print('Temp={0:0.1f}*C' 'Humidity={1:0.1f}%'.format(temperature2,humidity2))
    else:
        print('Failed to get readings. Try again')


    flag_2=0
    if temperature > 40:           #relay 2 for BMS heat reducing i.e on the fan/cooling device
        GPIO.output(relay_2,True)
        flag_2=1
    else:
        GPIO.output(relay_2,False)
    
#-------------------------------------------------------------------------------------------#
    flag_3=0
    if (temperature or temperature2) >=47:        #relay 3 for emergency stop
        flag_3=1

#-------------------------------------------------------------------------------------------#
    #gas sensor for detection of harmful gaseous
    gvalue=0
    vals=GPIO.input(gas)
    if vals>0:
        gvalue=1

#-------------------------------------------------------------------------------------------#
    #IR sensor for insects 
    val=GPIO.input(ir)
    if val==1:
        signal=0
    else:
        signal=1

 #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#      
    #This code is for taking the all sensors outputs and upload on the ThingSpeak Cloud 
    #and these all values save on the cloud & the .csv file obtained from it and we can train it on jupyter or tensorflow 
    time.sleep(10)
    f=urllib.request.urlopen("https://api.thingspeak.com/update?api_key=6FSQDLGVJQ2WYAQ7&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s&field8=%s"%(temperature,flag_1,temperature2,flag_2,signal,gvalue,hm,flag_3))
    print(f.read())
    f.close()    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    if flag_3==1:
        GPIO.output(relay_3,True)   #emergency stop
        exit()

#-------------------------------------------------------------------------------------------#

#main function call
while True:

    sensors_code()
#-------------------------------------------------------------------------------------------#