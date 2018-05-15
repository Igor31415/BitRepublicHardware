import json
import time
import random
import requests
from threading import Thread
import RPi.GPIO as GPIO
from blessings import Terminal

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setup(13, GPIO.OUT)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class BitsoilGenerator(Thread):
    def __init__(self, headers):
        Thread.__init__(self)
        self.headers = headers
        self.config = json.load(open('/home/pi/bitrepublic/Config.json'))
        self.address = self.config["requests"]["genBitSoil"]["Address"]
        #self.p = GPIO.PWM(13, 100)
        #self.p.start(0)
        self.t = Terminal()
        self.oldState = False
        print(self.t.bold('Hi there! : I\'m the Bitsoil Generator'))
    def run(self):
        while True:
            input_state = GPIO.input(17)    
            if(!self.oldState && input_state):
                print("ACTION")
            self.oldState = input_state
            
            time.sleep(0.33)
            #print(self.t.bold('BitsoilGenerator : is there any body here ?'))
            #r = requests.get(self.address, headers=self.headers)                #send the get request.
            #if r.status_code==200:                                              #checks if the server respond
            #    jdata = r.json()
            #    if jdata["data"]!=False:                                        #checks if there is data in the output of the server.
            #        print(self.t.bold('Fandriver : Yes ! so let the wind blow your mind'))
            #        self.p.ChangeDutyCycle(100)
            #        time.sleep(5)
                    #p.stop()
                    #GPIO.cleanup()
            #self.p.ChangeDutyCycle(0)
            #t = random.randint(2, 6)
            #print(self.t.bold('Fandriver : I need a small nap.'))
            #time.sleep(t)
