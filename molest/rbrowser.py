"""download resources from www.renren.com."""
import urllib.request as http#instead of urllib2
import urllib.parse #urlencode is used
import http.cookiejar as cookie
import re
import time
import uuid
from threadpool import ThreadPool

import mytools #used to get passwd from personal mysql

urlprog={
	'status':'http://status.renren.com/status?curpage={}&id={}&__view=async-html',
	'friendList':"http://friend.renren.com/GetFriendList.do?curpage={}&id={}",
	'profileInfo':"http://www.renren.com/{}/profile?v=info_ajax"}
itemprog={
	'status':re.compile(r'id="status-.+?ilike_icon'),
	'friendList':re.compile(r'<dd><a\s+href=\"http://www.renren.com/profile.do\?id=\d+\">.+?<\/a>'),
	'profileInfo':re.compile(r'<dl class="info">.+?</dl>')}

_timeout=3.0
#resend=3

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

_uppage=100
def friendList(rid):
	"""friendList('234234') --> ProfileUrls,nPage,nLastPage"""
	friendList=set()
	for curpage in range(_uppage):
		try:
			fstart=time.time()
			rsp=_opener.open(urlprog['friendList'].format(curpage,rid))
			pause=time.time()
			html_content=rsp.read().decode('UTF-8','ignore')
			fstop=time.time()
		except Exception as e:
			print('error')
		else:
			item_curpage=itemprog['friendList'].findall(html_content)
			print('friendList: renrenId={}, curpage={}, items={}, timecost1={},timecost2={}'.format(rid,curpage,len(item_curpage),pause-fstart,fstop-pause))
			if len(item_curpage) < 1:#all pages request$
				break
			else:
				friendList.update(item_curpage)
				n=len(item_curpage)
	return friendList,curpage,n

if __name__=='__main__':
	login()
	nThread=1
	tp=ThreadPool(nThread)
	start=time.time()
	for i in range(10):
		tp.add_job(friendList,'230760442')#wei
		tp.add_job(friendList,'250068531')#ju
		tp.add_job(friendList,'242934804')#wei
		tp.add_job(friendList,'233960464')#wei
	#tp.add_job(friendList,'287286312')
	#tp.add_job(friendList,'240303471')
	tstop=time.time()
	tp.wait_for_complete()
	stop=time.time()
	print(stop-start)
