#download resources from www.renren.com.
import urllib.request as http#instead of urllib2
import urllib.parse #urlencode is used
import http.cookiejar as cookie
import socket
import re
import os
import logging
import time
import uuid

import mytools #used to get passwd from personal mysql

class RenrenBrowser:
	urlTmplt={
		'status':'http://status.renren.com/status?curpage={}&id={}&__view=async-html',
		'friendList':"http://friend.renren.com/GetFriendList.do?curpage={}&id={}",
		'profile':"http://www.renren.com/{}/profile?v=info_ajax"}
	itemReg={
		'status':r'id="status-.+?ilike_icon',
		'friendList':re.compile(r'<dd><a\s+href=\"http://www.renren.com/profile.do\?id=\d+\">.+?<\/a>')}

	timeout=20.0
	resend=3

	def __init__(self,user='jiekunyang@gmail.com',path='.'):
		self.pwdRoot=path+"/renrenData"
		logPath=self.pwdRoot+'/spideLog'
		self.log=self.interfaceLog('renrenBrowser',logPath)
		#get passwd from mysql database, which is not necessary
		passwd=mytools.getPasswd('renren',user)
		self.login(user,passwd)
		socket.setdefaulttimeout(self.timeout)
		self.autoSave=False

	def friendList(self,renrenId='285060168',targetPage=None, uppage=100):
		pageStyle='friendList'
		if targetPage==None:
			return self.iterPage(pageStyle,renrenId,uppage)
		else:
			self.log.info('request 1 {} page of renrenId={},curpage={}'.format(pageStyle,renrenId,targetPage))
			return self.onePage(pageStyle,renrenId,targetPage)
	def status(self,renrenId=None,targetPage=None, uppage=100):
		pageStyle='status'
		if targetPage==None:
			return self.iterPage(pageStyle,renrenId,uppage)
		else:
			self.log.info('request 1 {} page of renrenId={},curpage={}'.format(pageStyle,renrenId,targetPage))
			return self.onePage(pageStyle,renrenId,targetPage)
	def profile(self,renrenId):
		pageStyle='profile'
		self.log.info('request {} of renrenId={}'.format(pageStyle,renrenId))
		return self.onePage(pageStyle,renrenId)

	def onePage(self,pageStyle=None,renrenId=None,curpage=None):
		traceId=uuid.uuid1()
		#construct url, if page=None, no page parmater needed.
		if curpage==None:
			url=self.urlTmplt[pageStyle].format(renrenId)
		else:
			url=self.urlTmplt[pageStyle].format(curpage,renrenId)
		#send request and decode response. auto resend 3 times, if time out.
		try:
			self.log.debug('request | success | url={}, traceId={} '.format(url,traceId))
			startTime=time.time()
			rsp=self.opener.open(url)
			htmlStr=rsp.read().decode('UTF-8','ignore')
			stopTime=time.time()
			self.log.debug('rsponse | success | timecost={}, traceId={} '.format(stopTime-startTime,traceId))
		except Exception as e:
			self.log.error('rsponse | time out | url={}, traceId={} '.format(url,traceId))
		#TODO: deal with resend
			htmlStr='timeout'

		#local storage if needed
		if self.autoSave:
			filename='{}{}_{}.html'.format(pageStyle, renrenId, curpage)
			self.savePage(filename,htmlStr)
		return htmlStr
	def iterPage(self,pageStyle=None,renrenId=None,uppage=100):
		itemsAll=set()
		self.log.debug('request {} of renrenId={}'.format(pageStyle,renrenId))
		start=time.time()
		for curpage in range(uppage+1):
			#request one page
			htmlStr=self.onePage(pageStyle,renrenId,curpage)
			#if timeout, pass
			if htmlStr=='timeout':continue
			#judge whether to go on or not
			itemsInPage=self.itemReg[pageStyle].findall(htmlStr)
			if len(itemsInPage) < 1:#all pages request
				stop=time.time()
				self.log.info('{} of renrenId={} has {} pages, total items: {}, time cost: {}'.format(pageStyle,renrenId,curpage, len(itemsAll), stop-start))
				break
			else:
				itemsAll=itemsAll | set(itemsInPage)
		return itemsAll
	def login(self,user,passwd):
		login_page = "http://www.renren.com/PLogin.do"
		try:
			#construct http request
			cj = cookie.CookieJar();
			self.opener=http.build_opener(http.HTTPCookieProcessor(cj));
			self.opener.addheaders=[('User-agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0')];
			data = urllib.parse.urlencode({"email":user,"password":passwd})
			data=data.encode(encoding='UTF8');#encoding is needed in python3.2

			#send request and decode response
			rsp=self.opener.open(login_page,data)
			homePage=rsp.read().decode('UTF-8','ignore')

			#check whether login is successful. 
			#paser response to find titlePtn
			titlePtn=r'<title>\w+\s+-\s+.+</title>'
			title=re.compile(titlePtn).findall(homePage)
			namePtn=r'-\s+.+<'
			name=re.compile(namePtn).findall(title[0])[0].strip('-<')
			self.log.info("user login successfully,name={},email={}".format(name,user))
			#return renrenId if login successful.
			renrenId='233330059'
		except Exception as e:
			#TODO:deal with type of exception. login error or time out.
			#TODO:raise exception
			self.log.error("user login failed,email={},msg={}".format(user,str(e)))
			renrenId='0'
		return renrenId

	def interfaceLog(self,objName, pwdLog):
		#init pwd and logfile name. 
		pwd=pwdLog
		if os.path.exists(pwd)==False:
			os.makedirs(pwd)
		logfile=pwd+'/'+objName+".log"
		#init logger
		logger=logging.getLogger('interface.{}'.format(objName))
		hdlr=logging.FileHandler(logfile)
		formatter=logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
		hdlr.setFormatter(formatter)
		logger.addHandler(hdlr)
		logger.setLevel(40)#20 info, 40 error
		return logger
	def setLogLevel(self,level):
		self.log.setLevel(level)#info 20, debug 10

	def savePage(self, filename, htmlStr, path=None):
		if path==None:
			pwd=self.pwdRoot+'/pages'
		else:
			pwd=path
		if os.path.exists(pwd)==False:
			os.makedirs(pwd)
			self.log.debug("mkdir {}".format(pwd))
		f=open(pwd+'/'+filename,'w')
		f.write(htmlStr)
		f.close()
	def localSave(self,flag):
		self.autoSave=flag
