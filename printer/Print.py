#!/usr/bin/python

from Adafruit_Thermal import *                  #https://github.com/adafruit/Python-Thermal-Printer/blob/master/Adafruit_Thermal.py
from PIL import Image
import requests                                 #see answer https://stackoverflow.com/questions/25491090/how-to-use-python-to-execute-a-curl-command
import time                                     #https://www.tutorialspoint.com/python/time_sleep.htm
import random                                   #https://openclassrooms.com/forum/sujet/python-fonction-randint-et-librairie-random-82775
import json
from threading import Thread
from blessings import Terminal

class Printer(Thread):
	def __init__(self, headers):
		Thread.__init__(self)
		
		self.headers = headers
		self.config = json.load(open('/home/pi/bitrepublic/Config.json'))
		self.printerCount = self.config["printer"]["count"]
		self.maxRequestPerSecond = self.config["printer"]["maxRequestPerSecond"]
		self.img = Image.open(self.config["printer"]["img"])
		self.address = self.config["requests"]["consume"]["Address"]
		self.minInterval = self.config["printer"]["minInterval"]  
		self.maxInterval = max(1, 2*self.printerCount*self.maxRequestPerSecond-self.minInterval)
		self.printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
															
		tmp = min(self.minInterval, self.maxInterval)
		self.maxInterval=max(self.minInterval, self.maxInterval)
		self.minInterval=tmp

		#print("minInterval : "+str(minInterval))
		#print("maxInterval : "+str(maxInterval))

		printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
		#print("Setup: success")
		self.t = Terminal()
		print(self.t.italic('Hi there! : I\'m the Printer'))

	def grabBitsoilAndPrint(self):
		print(self.t.italic('Printer : is there any new bitsoil ?'))
		r = requests.get(self.address, headers=self.headers)                          #send the get request.
		if r.status_code==200:                                              #checks if the server respond
			jdata = r.json()
			if jdata["data"]!=False:                                        #checks if there is data in the output of the server.
				print(jdata["data"])
				myDate = (jdata["data"]["date"])
				myKey = (jdata["data"]["publicKey"])
				myAmount = (jdata["data"]["bitsoil"])           
				print(self.t.italic('Printer : Yes ! so I\'ve to do...'))
				self.printReceipt(myDate, myKey, myAmount)
				
		else :
			print(r.status_code)

	def printReceipt(self,myDate, myKey, myAmount):
		self.printer.wake()                                                      # Call wake() before printing again, even if reset.

		self.printer.justify('C')
		self.printer.boldOn()
		self.printer.println(myDate)
		self.printer.boldOff()

		self.printer.println('')

		self.printer.justify('C')
		self.printer.println(myKey)

		self.printer.printImage(self.img, True)

		self.printer.setSize('M')
		self.printer.justify('C')
		self.printer.println (format(myAmount, 'f') + ' Bitsoil')
		self.printer.println('--------------------------------')

		self.printer.feed(1)

		self.printer.sleep()                                                     # Tell printer to sleep.
		self.printer.setDefault()                                                # Restore printer to defaults.
		self.printer.reset()                                                     #if you don't reset, the printer starts to fuck up the receipt.

	def run(self):
		while True:
			self.grabBitsoilAndPrint()                                    #checks if there is bitsoils available to print, and if there is, it prints it.
			t=random.randint(self.minInterval, self.maxInterval)
			print(self.t.italic('Printer : Pfiouf... See you in ' + str(t) + ' seconds'))
			time.sleep(t)                                                   #wait for x seconds before re-checking for bitsoils.