import urllib.request as http#instead of urllib2
import urllib.parse #urlencode is used
import http.cookiejar as cookie
import re
import time
import logging
import os

import mytools #used to get passwd from personal mysql

class RenrenBrowser:
	pwdRoot='/home/jackon/renrensite'
	pwdFriendPage=pwdRoot+'/friendPages'
	pwdProfilePage=pwdRoot+'/profilePages'
	pwdLog=pwdRoot+'/log'
	def __init__(self,user='jiekunyang@gmail.com'):

		self.log=self.initLogger()
		#get passwd from mysql database, which is not necessary
		self.user=user
		self.passwd=mytools.getPasswd('renren',user)

	def friendPage(self,renrenId='285060168',uppage=100):
		pwd=self.pwdFriendPage+'/{}'.format(renrenId)

		#only useful page is writtern, no end+1 page, no permision denied page
		self.log.info("start to get friendPage of {}".format(renrenId))
		#init pwd to write
		if os.path.exists(pwd)==False:
			os.makedirs(pwd)	
			self.log.debug("mkdir {}".format(pwd))

		#request pages which not existe locally
		urlTemplate="http://friend.renren.com/GetFriendList.do?curpage={}&id={}"
		filenameTemplate='friendPage_{}_{}.html'#id,page
		for page in range(len(os.listdir(pwd)),uppage+1):
			if(page==51):
				self.log.info('processing friendPage, getting page{} of {}'.format(page,renrenId))
			#send request and decode response
			self.log.debug("requesting friendPage, page={}, renrenId={}".format(page,renrenId))
			rsp=self.opener.open(urlTemplate.format(page,renrenId))
			self.log.debug("friendPage recieved , page={}, renrenId={}".format(page,renrenId))
			htmlStr=rsp.read().decode('UTF-8','ignore')

			urlPtn=r'<a\shref=\"http://www.renren.com/profile.do\?id=\d+\">'
			profileUrls=set(re.compile(urlPtn).findall(htmlStr))
			if len(profileUrls) < 2:
				#end of friend list page or permision denied
				self.log.debug("all friendPage of {} saved in {}".format(renrenId,pwd))
				break
			else:
				#write to file
				filename=pwd+'/'+filenameTemplate.format(renrenId,page)
				f=open(filename,'w')
				f.write(htmlStr)
				f.close()
				self.log.debug("friendPage writtern to file,filename={}".format(filename))
	def profilePage(self,renrenId):
		url_template="http://www.renren.com/{}/profile?v=info_ajax"
		#sending request and decode response
		self.log.debug("requesting detail profile, renrenId={}".format(renrenId))
		rsp=self.opener.open(url_template.format(renrenId))
		self.log.debug("detail profile recieved, renrenId={}".format(renrenId))
		htmlStr=rsp.read().decode('UTF-8','ignore')
		#init pwd to write
		pwd=self.pwdProfilePage
		if os.path.exists(pwd)==False:
			os.makedirs(pwd)	
			self.log.debug("mkdir {}".format(pwd))
		#write to file
		filenameTemplate='profile_{}.html'#id
		filename=pwd+'/'+filenameTemplate.format(renrenId)
		f=open(filename,'w')
		f.write(htmlStr)
		f.close()
		self.log.debug("detail profile write to file, file={}".format(filename))

	def login(self):
		user=self.user;
		passwd=self.passwd
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
			return '233330059'
		except Exception as e:
			self.log.error("user login failed,email={},msg={}".format(user,str(e)))
			return '0'

	def initLogger(self):
		pwd=self.pwdLog

		#init pwd to write
		if os.path.exists(pwd)==False:
			os.makedirs(pwd)	
		#init logfile name
		date=time.strftime("%Y%m%d", time.localtime())
		logfile=pwd+'/'+"renrenBrowser_{}.log".format(date)
		#init logger
		logger=logging.getLogger()
		hdlr=logging.FileHandler(logfile)
		formatter=logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
		hdlr.setFormatter(formatter)
		logger.addHandler(hdlr)
		logger.setLevel(20)#info
		return logger
	def setLogLevel(self,level):
		oldLevel=self.log.getEffectiveLevel()
		self.log.setLevel(level)#info 20, debug 10
		self.log.info("log level chanaged, from {} to {}".format(oldLevel,level))
