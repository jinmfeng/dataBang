#test data
#type of job, classify by resource that consumes most: I/O(file,internet,cpu,memory)
#number and type of job parameters
#style of par transfer to job, tuple/dict/one element
#run time of time cost by each single job, which will definately influence the peak number of thread.
#return type and value of job

from threadpool import ThreadPool
import time


def download(url,expt):
	#print('download {} start {}'.format(url,time.time()-start))
	dstart=time.time()
	rsp=request(url)
	#print('getNet1 of {}'.format(rid[0]))
	#TODO:deal with rsp
	dstop=time.time()
	if dstop-dstart>expt:
		print('download {} cost {} stop at {}'.format(rsp,dstop-dstart,dstop-start))
	return rsp

def request(url):
	#print('request {} at {}'.format(url,time.time()-start))
	time.sleep(0.13)
	#print('recieve {} at {}'.format(url,time.time()-start))
	return url

def test(nJob,nThread,expt):
	#test data:10 jobs,3 threads 
	tp = ThreadPool(nThread)
	tstart=time.time()
	for i in range(nJob):
		tp.add_job(download, i,expt)
	tstop=time.time()
	#print('{} cost to add {} jobs'.format(tstop-tstart,nJob))
	tp.wait_for_complete()
	stop=time.time()
	return tstop-tstart,stop-tstart

if __name__=='__main__':
	start=time.time()
	#job=18*400
	job=100
	for thread in range(1,20,5):
		addTime,total=test(job,thread,0.14)
		ideal=job*0.13/thread
		print('{} thread, actualCost={}, ideal={}, delta={}'.format(thread,total,ideal,total-ideal))
