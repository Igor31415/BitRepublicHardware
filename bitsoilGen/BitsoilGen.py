import json
import time
import random
import requests
from threading import Thread
import threading
import Queue
import RPi.GPIO as GPIO
from blessings import Terminal

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setup(13, GPIO.OUT)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

q = Queue.Queue()

class QueueGen(object):
    def __init__(self, headers):
        self.headers = headers
        self.config = json.load(open('/home/pi/bitrepublic/Config.json'))
        self.address = self.config["requests"]["genBitSoil"]["Address"]
        self.thread = threading.Thread(target=self.loop)
        # thread.daemon = True
        self.thread.start()

    def loop(self):
        while True:
            time.sleep(3)
            if not q.empty():
                r = requests.post(self.address, headers=self.headers)                          #send the get request.
                if r.status_code==200:                                              #checks if the server respond
                    q.get()
                    print("BITSOIL Generated")
                else : 
                    print("error")


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
        QueueGen(headers)
    def run(self):
        while True:
            input_state = GPIO.input(17)    
            if(self.oldState == False and input_state):
                print("ACTION")
                q.put("genbitsoil")
            self.oldState = input_state
            
            time.sleep(0.33)