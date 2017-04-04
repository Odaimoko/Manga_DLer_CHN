from threading import *
import time
import comiccrawler

class pauset:
	def __init__(self):
		self.running = 1

	def terminate(self):
		self.running = 0

	def loop(self):
		print('thread %s is running...' % current_thread().name)
		n = 0
		while not int(self.running) == 0:
			n = n + 1
			print('thread %s >>> %s' % (current_thread().name, n))
			time.sleep(1)
		print('thread %s ended.' % current_thread().name)
c=pauset()
t1 = Thread(target=c.loop)
t1.start()
while True:
	b=input()
	c.running=b
