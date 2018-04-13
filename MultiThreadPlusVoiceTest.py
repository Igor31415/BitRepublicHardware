import subprocess
from threading import Thread
import time

class ThreadTest(Thread):
	def __init__(self, words):
		Thread.__init__(self)
		self.words = words
		
	def run(self):
		while True:
			args = ['espeak', self.words]
			subprocess.Popen(args)
			time.sleep(10)
			
		
class ThreadLoop(Thread):
	def __init__(self):
		Thread.__init__(self)
		
	def run(self):
		x=1
		while True:
			print(x)
			x+=1
			time.sleep(1)
				
		
thread_1 = ThreadTest("I want to eat some tasty bitsoils")
thread_2 = ThreadLoop()
thread_1.daemon = True
thread_2.daemon = True
thread_1.start()
thread_2.start()

while True:
	time.sleep(1)