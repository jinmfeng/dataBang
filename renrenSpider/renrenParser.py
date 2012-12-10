import re
import time
import logging
import os
from renrenDb import *
from renrenBrowser import * 

class RenrenParser:
	def __init__(self):
#		self.log=self.initLogger()
		pass

	def friendPage(self,filename):
		#open and read 
		f=open(filename,'r')
		htmlStr=str(f.readlines())

		#parser all id/name pairs from profile urls
		urlPtn=r'<a\shref=\"http://www.renren.com/profile.do\?id=\d+\">[^<]+<\/a>'
		profileUrls=set(re.compile(urlPtn).findall(htmlStr))
		pairs=set()
		for item in profileUrls:
			renrenId=re.compile(r'=\d+\"').findall(item)[0].strip('="')
			name=re.compile(r'>[^<]+<').findall(item)[0].strip('<>')
			pairs.add((renrenId,name))
		return pairs

	def friends(self):
		for renrenId in os.listdir(RenrenBrowser.pwdFriendPage):
			pwd=RenrenBrowser.pwdFriendPage+'/'+renrenId+'/'

			#parsered pages and assign to flist 
			pages=os.listdir(pwd)
			flist=set()
			#files that parsering, store for rename later
			parsering=[]
			for page in pages:
				if page.find('parsered_')==0:
					#file parserd, continue
					continue
				else:
					parsering.append(page)
					flist= flist| self.friendPage(pwd+page)

			if len(pages)==0:
				#if empty, mkdir flag file and assign 1 to flist
				os.mknod(pwd+'parsered_{}_noPermision.html'.format(renrenId))
				flist={('1','unavailable')}
			elif len(flist)==0:
				#all files parser, continue
				continue
			#else:
			#insert into table, pairs>temp_profile, relation>temp_relation
			db=RenrenDb()	
			sqlProfile='insert into {} (renrenId,name) values {}'.format(db.temp_profile,str(flist).strip('{}'))
			relation=''
			for pair in flist:
				relation=relation+'({},{}),'.format(renrenId,str(pair[0]))
			sqlRelation='insert into {} (renrenId1,renrenId2) values {}'.format(db.temp_relation,relation.strip(','))
			conn=db.getConn()
			cur=conn.cursor()
			m=cur.execute(sqlProfile)
			n=cur.execute(sqlRelation)
		#	self.log.info('{} profiles and {} relations of {} inserted into db'.format(m,n,renrenId))
			conn.commit()
			cur.close()
			conn.close()
	
			#rename parsering files
			for old in parsering:
				new='parsered_'+old
				os.rename(pwd+old,pwd+new)
			
	def initLogger(self):

		#init pwd to write
		pwd=RenrenBrowser.pwdLog
		if os.path.exists(pwd)==False:
			os.makedirs(pwd)	
		#init logfile name
		date=time.strftime("%Y%m%d", time.localtime())
		logfile=pwd+'/'+"renrenParser_{}.log".format(date)
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
