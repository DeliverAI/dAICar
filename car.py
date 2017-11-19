import RPi.GPIO as GPIO
from time import sleep
from box import openBox
import json
import requests

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22

Motor2A = 19
Motor2B = 21
Motor2E = 23

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

GPIO.setup(18, GPIO.OUT)


def driveForward(time):

    print "Going forwards"
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)

    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.HIGH)

    sleep(time)


def turnLeft(time):

    print "Turnning"
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)

    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.HIGH)

    sleep(time)



while(True):
    r = requests.get(
        'https://hackwestern-8e5fa.firebaseio.com/who_ordered/order_made.json')
    if(r.json()):
        address = requests.get(
            'https://hackwestern-8e5fa.firebaseio.com/who_ordered/address.json')

        car_instructions = requests.get(
            'https://hackwestern-8e5fa.firebaseio.com/car_instructions.json')
        json_data = json.loads(car_instructions.text)
        try:
            instructions = json_data[address.text.encode(
                'utf8').replace("\"", "")]
        except KeyError, e:
            instructions = json_data['1 University Road']

        left = instructions['left']
        forward = instructions['forward']

        GPIO.setmode(GPIO.BOARD)

        turnLeft(left)
        driveForward(forward)

        GPIO.output(Motor1E, GPIO.LOW)
        GPIO.output(Motor2E, GPIO.LOW)
        GPIO.cleanup()

        requests.patch('https://hackwestern-8e5fa.firebaseio.com/.json',
                       data=json.dumps({"package_arrived": True}))

        openBox()


# print "Going backwards"
# GPIO.output(Motor1A,GPIO.LOW)
# GPIO.output(Motor1B,GPIO.HIGH)
# GPIO.output(Motor1E,GPIO.HIGH)
#
# GPIO.output(Motor2A,GPIO.LOW)
# GPIO.output(Motor2B,GPIO.HIGH)
# GPIO.output(Motor2E,GPIO.HIGH)
#
# sleep(2)
#
#
# print "Now stop"
# GPIO.output(Motor1E,GPIO.LOW)
# GPIO.output(Motor2E,GPIO.LOW)
#
# GPIO.cleanup()
