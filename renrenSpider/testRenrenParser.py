import unittest

from renrenParser import *
from renrenCache import *
#from renrenBrowser import *

class TestRenrenParser(unittest.TestCase):

	def setUp(self):
		self.data=RenrenCache()
		self.parser=RenrenParser(self.data)

		#browser=RenrenBrowser()
		#browser.login()

		#test data
		self.flist=[{'<dd><a href="http://www.renren.com/profile.do?id=266754031">王瑛</a>', '<dd><a href="http://www.renren.com/profile.do?id=27331442">Ethan.王哲</a>', '<dd><a href="http://www.renren.com/profile.do?id=240303471">刘洋English</a>'},{'<dd><a href="http://www.renren.com/profile.do?id=239439171"></a>','<dd><a href="http://www.renren.com/profile.do?id=222439171">eeee</a>'},{'<dd><a href="http://www.renren.com/profile.do?id=324134134">～！@#￥%……&*（）</a>'},{}]
		self.renrenId=['111111','22222','33333','44444']
		self.names=[{'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English'},{'239439171':'','222439171':'eeee'},{'324134134':'～！@#￥%……&*（）'},{}]

	def tearDown(self):
#		self.browser.dispose()
		self.parser=None

	def testFriendList(self):
		fl=dict()
		name=dict()
		for i in range(0,len(self.renrenId)):
			fl[self.renrenId[i]]=set(self.names[i].keys())
			name.update(self.names[i])
			self.parser.friendList(self.renrenId[i],self.flist[i])
		self.assertEquals(self.data.getAttrData('friendList'),fl)
		self.assertEquals(self.data.getAttrData('name'),name)

if __name__=='__main__':
	suite=unittest.TestSuite()
	suite.addTest(TestRenrenParser('testFriendList'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
