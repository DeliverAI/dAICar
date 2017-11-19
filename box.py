import RPi.GPIO as GPIO
from time import sleep
import requests
import json

def openBox():
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(18, GPIO.OUT)
    pwm = GPIO.PWM(24, 50)
    pwm.start(1)
    flag = True

    while(flag):
        r = requests.get('https://hackwestern-8e5fa.firebaseio.com/package_unlock.json')
        if(r.json()):
            pwm.ChangeDutyCycle(8)
            sleep(10)
            requests.patch('https://hackwestern-8e5fa.firebaseio.com/.json', data = json.dumps({"package_unlock": False}))
            # print(r.json())
        else:
            # print("Hello!")
            pwm.ChangeDutyCycle(1)
            flag = False
        sleep(1)
