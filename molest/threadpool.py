"""a module for multi-thread management.

the simplest way to use this module:
1. tp=ThreadPool(nThread) #init thread pool
2. tp.add_job(meth_ame,vars) #vars is parameters of method math_name
3. tp.wait_for_complete()#all jobs done by multi-thread

"""
import queue 
import threading
import sys
import time
import urllib

#thread obj in thread pool
class MyThread(threading.Thread):
	def __init__(self, workQueue, resultQueue,timeout=2):
		threading.Thread.__init__(self)
		self.timeout = timeout#time that a thread wait for a queue
		self.setDaemon(True)#stop with main thread
		self.workQueue = workQueue
		self.resultQueue = resultQueue
		self.start()
	def run(self):
		#continuously run until workQueue empty
		while True:
			try:
				#get a job from workQueue, do it and add res to resultQueue
				callable, args=self.workQueue.get(timeout=self.timeout)
				#print('{} running, job={}, parameters={}'.format(self.getName(),callable,args))
				res = callable(*args)
				#self.resultQueue.put( (res,self.getName()) )
				self.resultQueue.put( (res,callable,args) )
			except queue.Empty:
				break

class ThreadPool:
	def __init__(self,num_of_threads=10):
		self.workQueue = queue.Queue()
		self.resultQueue = queue.Queue()
		self.threads = []
		self.__createThreadPool(num_of_threads)
	def __createThreadPool(self, num_of_threads):
		for i in range(num_of_threads):
			thread = MyThread(self.workQueue, self.resultQueue)
			self.threads.append(thread)
	def wait_for_complete(self):
		while len(self.threads):
			thread = self.threads.pop()
			if thread.isAlive():
				thread.join()
	def add_job(self, callable, *args):
		self.workQueue.put( (callable,args) )

	def get_res(self,meth_name):
		self.wait_for_complete()
		res=dict()
		while True:
			try:
				job_res,job_name,job_args=self.resultQueue.get(timeout=2)
				if job_name is meth_name:
					res[job_args]=job_res
			except queue.Empty:
				break
		return res

