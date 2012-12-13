import re
import time
import os
from renrenDb import *

class PageParser:
	def __init__(self):
#		self.log=self.initLogger()
		pass

	def statusPage(self,filename,mainId=None):
		#open and read 
		f=open(filename,'r')
		htmlStr=str(f.readlines())
		f.close()

		#parser all id/name pairs from profile urls
		#itemPtn=r'<a\shref=\"http://www.renren.com/profile.do\?id=\d+\">[^<]+<\/a>'
		itemPtn=r'id="status-.+?ilike_icon'
		itemList=re.compile(itemPtn).findall(htmlStr)
		status=''
		for item in itemList:
			#statusId, content, duration, replycount
			statusIdPtn=r'"status-\d+">'
			statusId=re.compile(statusIdPtn).findall(item)[0].replace('status','').strip('-=<>"')

			contentPtn=r'<h3>.+</h3>'
			contentDraft=re.compile(contentPtn).findall(item)[0]
			#simplify content
			#no @ href
			atHrefPtn=r"<a\s+href=\\'http://www.renren.com/g/\d+.+?>"
			hrefs=re.compile(atHrefPtn).findall(contentDraft)
			for href in hrefs:
				#print(href)
				renrenId=re.compile(r'\d+').findall(href)[0]
				contentDraft=contentDraft.replace(href,'(renrenId={})'.format(renrenId))
			#no normal profile href
			profileHrefPtn=r'<a\shref="http://www.renren.com/profile.do\?id=.+?>'
			profile=re.compile(profileHrefPtn).findall(contentDraft)
			for href in profile:
				#print(href)
				renrenId=re.compile(r'\d+').findall(href)[0]
				contentDraft=contentDraft.replace(href,'(renrenId={})'.format(renrenId))
			#no public profile href
			profileHrefPtn=r'<a\shref="http://page.renren.com/.+?>'
			profile=re.compile(profileHrefPtn).findall(contentDraft)
			for href in profile:
				#print(href)
				renrenId=re.compile(r'\d+').findall(href)[0]
				contentDraft=contentDraft.replace(href,'(renrenId={})'.format(renrenId))
			#no alt img
			imgPtn=r"<img\s+src=.+?alt=\\'.+?\\'.+?/>"
			imgs=re.compile(imgPtn).findall(contentDraft)
			for img in imgs:
				#print(img)
				imgDesc=re.compile(r"\\'.+?\\").findall(img)[1].strip("=\\'")
				contentDraft=contentDraft.replace(img,'(img={})'.format(imgDesc))
			#no img in name
			nameImgPtn=r"<img class=.+?alt=.+?http://a.xnimg.cn/.+?/>"
			nameImg=re.compile(nameImgPtn).findall(contentDraft)
			for img in nameImg:
				#print(img)
				contentDraft=contentDraft.replace(img,'')
				#print(img,imgDesc)
			content=re.compile(r'>:.+</').findall(contentDraft)[0].replace('</a>','').replace('\\n','').strip("<>/:',\\ ")

			timePtn=r'"duration">.+?\\n'
			time=re.compile(timePtn).findall(item)[0]
			timestamp=re.compile(r'>.+\\n').findall(time)[0].strip('=<>"\\n')

			replyCountPtn=r'replyCount\d+">\(\d+\)'
			replyCountDraft=re.compile(replyCountPtn).findall(item)
			if len(replyCountDraft)<1:
					replyCount='0'
			else:
				replyCount=re.compile(r'\(\d+\)').findall(replyCountDraft[0])[0].strip('()')
			#status.append({'statusId':statusId,'timestamp':timestamp,'replyCount':replyCount,'content':content})
			#status={'statusId':statusId,'timestamp':timestamp,'replyCount':replyCount}
			status=status+",('{}','{}','{}','{}','{}')".format(statusId,mainId,content.replace("'",'"'),replyCount,timestamp)
		sql="INSERT INTO temp_status(statusId,renrenId,content,replyCount,timestamp) values {}".format(status.strip(','))
		#print(sql)
		db=RenrenDb()	
		conn=db.getConn()
		cur=conn.cursor()
		try:
			n=cur.execute(sql)
			conn.commit()
		except Exception as e:
			print('error. filename={}'.format(filename))
			print(sql)
			n=0
		cur.close()
		conn.close()
		return n
	def iterPage(self,filename,pageStyle=None):
		#open and read 
		f=open(filename,'r')
		htmlStr=str(f.readlines())
		f.close()
		#split into itemList
		itemPtn=r'id="status-.+?ilike_icon'
		itemList=re.compile(itemPtn).findall(htmlStr)
		#parser item with one regex ptn
		recordName=['statusId','content','timestamp','replyCount','renrenId']
		ptn=r'id="status-(?P<{}>\d+)">.*class="avatar"\s+namecard="(?P<{}>\d+).*<h3>(?P<{}>.+)</h3>.*"duration">(?P<{}>.+?)\\n.*replyKey.+?<span\s\w+="(?P<reply>replyCount)?(?(reply).+\((?P<{}>\d+)\))'.format(recordName[0],recordName[4],recordName[1],recordName[2],recordName[3])
		p=re.compile(ptn,re.DOTALL)
		sql="INSERT INTO {} ({}) values".format('orig_renren_status',str(recordName).replace("'",'').strip('{}[]]()'))
		for item in itemList:
			m=p.search(item)
			values=[]
			for record in recordName:
				values.append(m.group(record))
			if values[3]==None:
				values[3]=0
			sql=sql+"({}),".format(str(values).strip('{}[]()'))
		sql=sql.rstrip(',')

		db=RenrenDb()
		db.execute(sql)

	def status(self,pwdStatus):
		renrenIds=os.listdir(pwdStatus)
		for i,renrenId in zip(range(0,len(renrenIds)),renrenIds):
			pwd=pwdStatus+'/'+renrenId+'/'
			print('{}/{} parsering, renrenId={}'.format(i,len(renrenIds),renrenId))

			for page in os.listdir(pwd):
				try:
					self.iterPage(pwd+page,'statusPage')
				except Exception as e:
					print('error. filename={}'.format(page))


#a=RenrenParser()
#a.iterPage('/home/jackon/renrenData/status/265432635/status265432635_4.html')
