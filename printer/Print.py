#!/usr/bin/python

from Adafruit_Thermal import *                  #https://github.com/adafruit/Python-Thermal-Printer/blob/master/Adafruit_Thermal.py
from PIL import Image
import requests                                 #see answer https://stackoverflow.com/questions/25491090/how-to-use-python-to-execute-a-curl-command
import time                                     #https://www.tutorialspoint.com/python/time_sleep.htm
import random                                   #https://openclassrooms.com/forum/sujet/python-fonction-randint-et-librairie-random-82775
import json
import Tools

config = json.load(open('/home/pi/bitrepublic/Config.json'))
printerCount = config["printer"]["count"]
maxRequestPerSecond = config["printer"]["maxRequestPerSecond"]
address = config["requests"]["consume"]["Address"]                      #address to send the grabBitSoil request.
img = Image.open(config["printer"]["img"])                              #address of the image printed on the receipt.

minInterval = config["printer"]["minInterval"]                          #minimum value of the random.randint
maxInterval = max(1, 2*printerCount*maxRequestPerSecond-minInterval)    #maximum value of the random.randint
                                                                        # Be sure the minInterval is smaller than maxInterval
tmp = min(minInterval, maxInterval)
maxInterval=max(minInterval, maxInterval)
minInterval=tmp

print("minInterval : "+str(minInterval))
print("maxInterval : "+str(maxInterval))

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

accessKey = Tools.login()                                               #Get the function login (login to the api) from the Tools.py script
headers = {"X-Auth-Token": accessKey["authToken"] , "X-User-Id": accessKey["userId"]}

def grabBitsoilAndPrint():
    print("run")
    r = requests.get(address, headers=headers)                          #send the get request.
    if r.status_code==200:                                              #checks if the server respond
        jdata = r.json()
        print(jdata)
        if jdata["data"]!=False:                                        #checks if there is data in the output of the server.
            myDate = (jdata["data"]["date"])
            myKey = (jdata["data"]["publicKey"])
            myAmount = (jdata["data"]["bitsoil"])           

            printReceipt(myDate, myKey, myAmount)
    else :
        print(r.status_code)

def printReceipt(myDate, myKey, myAmount):
    printer.wake()                                                      # Call wake() before printing again, even if reset.
    
    centerText()
    printer.boldOn()
    printer.println(myDate)
    printer.boldOff()

    printer.println('')

    centerText()
    printer.println(myKey)

    printer.printImage(img, True)

    printer.setSize('M')
    centerText()
    printer.println (format(myAmount, 'f') + ' Bitsoil')
    printer.println('--------------------------------')

    printer.feed(1)

    printer.sleep()                                                     # Tell printer to sleep.
    printer.setDefault()                                                # Restore printer to defaults.
    printer.reset()                                                     #if you don't reset, the printer starts to fuck up the receipt.
    
def centerText():
    printer.justify('C')

def run():
    while True:
        grabBitsoilAndPrint()                                               #checks if there is bitsoils available to print, and if there is, it prints it.
        t=random.randint(minInterval, maxInterval)
        print("sleep " + str(t) + " seconds")
        time.sleep(t)                                                       #wait for x seconds before re-checking for bitsoils.