import rbrowser
import rdb
import threadPool
from rparser import *
import time

class RenrenSpider:
	def __init__(self,tablePre='orig'):
		self.parser=rParser()
		self.db=rdb.rDb(tablePre)
		self.browser=rbrowser.rBrowser()
		self.browser.setLogLevel(20)

		self.searched=self.db.getSearched('relation')

	def getNet1(self,renrenIds=('233330059',)):
		#force to get data from internet only.
		renrenId=renrenIds[0]
		start=time.time()
		name=self.parser.friendList(self.browser.friendList(renrenId))
		stop=time.time()
		#print('net1 of {} timecost: {}'.format(renrenId,stop-start))

		self.db.insertFriendList(renrenId,name)
		self.searched.add(renrenId)
		return set(name.keys())
	def getNet2(self,orig='233330059'):
		if orig in self.searched:
			target=self.db.getRenrenId(2,orig)
		else:
			target=self.getNet1(orig)
		toSearch=target-self.searched

		nThread=10
		#parallel
		tp=threadPool.ThreadPool(nThread)
		start=time.time()
		for renrenId in toSearch:
			tp.add_job(self.getNet1,renrenId)
		tp.wait_for_complete()
		stop=time.time()
		print('net2 of {} timecost: {}'.format(orig,stop-start))

if __name__=='__main__':
	spider=RenrenSpider()
	spider.getNet2('229837881')
