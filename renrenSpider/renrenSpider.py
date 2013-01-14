import renrenBrowser
import renrenDb
from renrenParser import *
import time

class RenrenSpider:
	def __init__(self,tablePre='orig'):
		self.parser=RenrenParser()
		self.db=renrenDb.RenrenDb(tablePre)
		self.browser=renrenBrowser.RenrenBrowser()
		self.browser.setLogLevel(20)
		self.db.createTables()

		self.searched=self.db.getSearched('relation')

	def getNet1(self,renrenId='233330059'):
		#force to get data from internet only.
		start=time.time()
		name=self.parser.friendList(self.browser.friendList(renrenId))
		stop=time.time()
		print('net1 of {} timecost: {}'.format(renrenId,stop-start))

		self.db.insertFriendList(renrenId,set(name.keys()))
		self.db.insertName(name)
		self.searched.add(renrenId)
		return set(name.keys())
	def getNet2(self,orig='233330059'):
		if orig in self.searched:
			target=self.db.getRenrenId(2,orig)
		else:
			target=self.getNet1(orig)
		toSearch=target-self.searched

		start=time.time()
		#parallel
		for renrenId in toSearch:
			name=self.parser.friendList(self.browser.friendList(renrenId))
			self.db.insertFriendList(renrenId,set(name.keys()))
			self.db.insertName(name)
			self.searched.union(toSearch)
		stop=time.time()
		print('net2 of {} timecost: {}'.format(orig,stop-start))

if __name__=='__main__':
	spider=RenrenSpider()
	spider.getNet2()
