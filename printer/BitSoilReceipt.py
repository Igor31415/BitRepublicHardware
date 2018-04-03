#!/usr/bin/python

from Adafruit_Thermal import * #https://github.com/adafruit/Python-Thermal-Printer/blob/master/Adafruit_Thermal.py
from PIL import Image
import requests #see answer https://stackoverflow.com/questions/25491090/how-to-use-python-to-execute-a-curl-command
import time #https://www.tutorialspoint.com/python/time_sleep.htm
import random #https://openclassrooms.com/forum/sujet/python-fonction-randint-et-librairie-random-82775

a = 1 #minimum value of the random.randint
b = 2 #maximum value of the random.randint

address = 'http://local.bitsoil.tax/api/bitsoil/consume' #address to send the curl request.
img = Image.open("Bitsoil_Logo384x384Flatened.png") #address of the image printed on the receipt.

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

def grabBitsoilAndPrint():
    r = requests.get(address) #send the get request.
    jdata = r.json()
    print(r.json())
    
    if r.status_code==200: #checks if the server respond
        if jdata["data"]!=False: #checks if there is data in the output of the server.
            myDate = (jdata["data"]["date"])
            myKey = (jdata["data"]["publicKey"])
            myAmount = (jdata["data"]["bitsoil"])           
            ''' 
            print(myDate)
            print(myKey)
            print(myAmount)
            ''' #multi-line comment.
            printReceipt(myDate, myKey, myAmount)

def printReceipt(myDate, myKey, myAmount):
    printer.wake()       # Call wake() before printing again, even if reset.
    #printer.reset() #if you don't reset, the printer starts to fuck up the receipt.
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

    printer.sleep()      # Tell printer to sleep.
    printer.setDefault() # Restore printer to defaults.
    printer.reset() #if you don't reset, the printer starts to fuck up the receipt.
    
def centerText():
    printer.justify('C')
    
while True:
    grabBitsoilAndPrint() #checks if there is bitsoils available to print, and if there is, it prints it.
    time.sleep(random.randint(a,b)) #wait for x seconds before re-checking for bitsoils.