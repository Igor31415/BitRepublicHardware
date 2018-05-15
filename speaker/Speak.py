import os
import json
import time
import random
import requests
import subprocess
from threading import Thread

class Speaker(Thread):
	def __init__(self, headers):
		Thread.__init__(self)
		self.headers = headers
		self.config = json.load(open('/home/pi/bitrepublic/Config.json'))
		self.address = self.config["requests"]["speaker"]["Address"]
		
	def run(self):
		while True:
			print("	Try to get Bitsoil to speak...")
			r = requests.get(self.address, headers=self.headers)                          #send the get request.
			if r.status_code==200:                                              #checks if the server respond
				jdata = r.json()
				print(jdata)
				if jdata["data"]!=False:                                        #checks if there is data in the output of the server.
					myDate = (jdata["data"]["date"])
					myKey = (jdata["data"]["publicKey"])
					myAmount = (jdata["data"]["bitsoil"])
					
					myAmount*=1000000.0
					processedMykey = list(myKey)
					pMykey = (" ").join(processedMykey)
					
					myPhrase = "A wallet have received: " + str(int(myAmount)) + "micro bitsoil"  
					args = ["espeak", "-ven+f3", "-s160", "-p55", myPhrase]
					
					subprocess.call(args, stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
					print("		Got Bitsoil to speak, and going to sleep.")
					time.sleep(12)
			time.sleep(random.randint(2, 6))
