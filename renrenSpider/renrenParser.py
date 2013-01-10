import re
import time
import logging
import os
from renrenCache import *

class RenrenParser:
	def __init__(self,data):
		self.data=data#RenrenCache()
#		self.log=self.initLogger()

	def friends(self,renrenId,items):
		friends=set()
		names=dict()
		for item in items:
			friendId=re.compile(r'=\d+\"').findall(item)[0].strip('="')
			name=re.compile(r'\">.+?<').findall(item)[0].strip('"<>')
			friends.add(friendId)
			names[friendId]=name
		if len(items)==len(friends):
			self.data.addItem('friends',renrenId,friends)
			self.data.addItems('name',names)
		else:
			print('{} friendList parser error'.format(renrenId))
				#self.log.error(

	def profile(self,renrenId,page):
		#parser out all <dt>tag</dt>\W*?<dd>value</dd>
		itemPtn=r'<dt>[^<]*?</dt>\W?<dd>.*?</dd>'
		items=re.compile(itemPtn,re.DOTALL).findall(page)

		ptn=re.compile(r'<dt>([^<]*?)</dt>\W?<dd>(.*?)</dd>',re.DOTALL)

		print('||||||||||||||||||||||||||||||||||||||')
		for item in items:
			#print("-------------\n{}".format(item))
			pair=ptn.match(item)
			tag=pair.group(1).strip(' \n')
			value=pair.group(2).strip(' \n')
			#drop useless info in value
			value=re.sub(r'<a\s[^>]+?>([^<]*?)</a>',r'\1',value)#drop superlink
			value=re.sub(r'(?:&nbsp;)|(?:\"\+response\.[a-z]+\+\")|\s+|\n+',r'',value)#drop \s,\n, non content string
			print("------------------\n{}{}".format(tag,value))
			#add to cache
