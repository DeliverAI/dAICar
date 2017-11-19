import RPi.GPIO as GPIO
from time import sleep
import requests
import json

def openBox():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)
    pwm = GPIO.PWM(12, 50)
    pwm.start(1)
    flag = True

    while(flag):
        r = requests.get('https://hackwestern-8e5fa.firebaseio.com/package_unlock.json')
        if(r.json()):
            pwm.ChangeDutyCycle(8)
            sleep(10)
            requests.patch('https://hackwestern-8e5fa.firebaseio.com/.json', data = json.dumps({"package_unlock": False}))
            pwm.ChangeDutyCycle(1)
            flag = False
            # print(r.json())

        sleep(1)
