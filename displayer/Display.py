# -*- coding: utf-8 -*-
# @Author: Evrard Vincent
# @Date:   2018-05-01 13:40:34
# @Last Modified by:   vincent
# @Last Modified time: 2018-05-02 18:41:32

import os
import json
import time
import random
import requests
import subprocess
from threading import Thread
import threading
import Queue

q = Queue.PriorityQueue()

class fillTheQueue(object):
	def __init__(self, headers):
		self.headers = headers
		self.config = json.load(open('/home/pi/bitrepublic/Config.json'))
		self.address = self.config["requests"]["displayer"]["Address"]
		self.oldData = None
		self.thread = threading.Thread(target=self.loop)
		# thread.daemon = True
		self.thread.start()

	def loop(self):
		while True:
			time.sleep(random.randint(5, 15))
			print("Try to get Wallets...")
			r = requests.get(self.address, headers=self.headers)                          #send the get request.
			if r.status_code==200:                                              #checks if the server respond
				jdata = r.json()
				
				if jdata["data"]!=False:                                        #checks if there is data in the output of the server.
					if self.oldData != jdata["data"]:
						for data in jdata["data"]:
							myKey = (data["publicKey"])
							myAmount = (data["bitsoil"])
							myId = (data["number"])
							myAmount*=1000000.0

							myPhrase = "The wallet " + myKey + " has " + str(int(myAmount)) + (" microBitsoils").decode("utf8")
							#myPhrase = "The user " + str(myId) + " has " + str(int(myAmount)) + " micro bitsoils"
							q.put((0, myPhrase))
							print("add : " + myPhrase)
						self.oldData = jdata["data"]

class Displayer(Thread):
	def __init__(self, headers):
		Thread.__init__(self)
		self.baseSentences = [
			"bitsoil.tax",
			"Make the data economy benefits all",
			"bitsoil.tax",
			"Bitsoil popup tax & hack campaign",
			"bitsoil.tax/campaign",
			"Claim a #BITSOILTAX",
			"Send your claim to the Prime Minister",
			"Time to net giants to pay",
			"join the bitsoil campaign",
			"take part of the redistribution",
			"Contact us : campaign@bitsoil.tax",
			"#Bitsoil is the new oil of the digital economy",
			"Claim your fair share of this world’s newest resource"
		]
		for sentence in self.baseSentences:
			q.put((random.randint(2, 2 + len(self.baseSentences)), sentence))

		fillTheQueue(headers)

	def run(self):

		while True:
			p, item = q.get()
			print("Display : " + str(p) + " - " +item)

			if p == 0:
				subprocess.call(self.buildRequest(item, 8), stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))	
			else :
				subprocess.call(self.buildRequest(item, random.randint(2, 20)), stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
				q.put((random.randint(p, p+2+len(self.baseSentences)), item))


	def buildRequest(self, sentence, speed=10, loop=1):
		return [
			"/home/pi/rpi-rgb-led-matrix/examples-api-use/scrolling-text-example", 
			"-f", "/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf",
			"--led-no-hardware-pulse",
			"--led-rows=32",
			"--led-cols=160",
			"--led-inverse",
			"-y", "16",
			"-C", "0,0,255",
			"-s", str(speed),
			"-l", str(loop),
			sentence
		]
#