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
