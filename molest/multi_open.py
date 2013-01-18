#test data
#type of job, classify by resource that consumes most: I/O(file,internet,cpu,memory)
#number and type of job parameters
#style of par transfer to job, tuple/dict/one element
#run time of time cost by each single job, which will definately influence the peak number of thread.
#return type and value of job

import urllib.request as http#instead of urllib2
import urllib.parse #urlencode is used
import http.cookiejar as cookie
import re
import time
import uuid

from threadpool import ThreadPool
import mytools

_opener=None
def login(user='yyttrr3242342@163.com',passwd=None):
	if passwd is None:
		passwd=mytools.getPasswd('renren',user)
	cj = cookie.CookieJar();
	opener=http.build_opener(http.HTTPCookieProcessor(cj));
	opener.addheaders=[('User-agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0')];
	data = urllib.parse.urlencode({"email":user,"password":passwd})
	data=data.encode(encoding='UTF8');#encoding is needed in python3.2
	
	login_page = "http://www.renren.com/PLogin.do"
	rsp=opener.open(login_page,data)
	print(rsp.geturl())
	rid=1
	global _opener
	_opener=opener
	return rid

def download(rid):
	#print('request {} at {}'.format(url,time.time()-start))
	urlprog={'friendList':"http://friend.renren.com/GetFriendList.do?curpage={}&id={}"}
	dstart=time.time()
	curpage=0
	rsp=_opener.open(urlprog['friendList'].format(curpage,rid))
	dstop=time.time()
	#print('recieve {} at {}'.format(url,time.time()-start))
	#print('download {} cost {} stop at {}'.format(rsp.geturl(),dstop-dstart,dstop-start))

def test(nJob,nThread,expt):
	#test data:10 jobs,3 threads 
	tp = ThreadPool(nThread)
	urlprog={'friendList':"http://friend.renren.com/GetFriendList.do?curpage={}&id={}"}
	curpage=0
	rid='233330059'
	url=urlprog['friendList'].format(curpage,rid)
	tstart=time.time()
	for i in range(nJob):
		tp.add_job(_opener.open, url)
	tstop=time.time()
	#print('{} cost to add {} jobs'.format(tstop-tstart,nJob))
	tp.wait_for_complete()
	stop=time.time()
	return tstop-tstart,stop-tstart

if __name__=='__main__':
	login()
	start=time.time()
	#job=18*400
	job=150
	for thread in range(1,76,25):
		addTime,total=test(job,thread,0.14)
		ideal=job*0.13/thread
		print('{} thread, actualCost={}, ideal={}, delta={}'.format(thread,total,ideal,total-ideal))
