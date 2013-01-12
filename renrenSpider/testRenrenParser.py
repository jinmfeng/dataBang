import unittest
import os

from renrenParser import *
from renrenBrowser import *

class TestRenrenParser(unittest.TestCase):

	def setUp(self):
		self.parser=RenrenParser()

	def tearDown(self):
#		self.browser.dispose()
		self.parser=None

	def testFriendList(self):
		#test data, num of items: 3/2/1/0/errorItem
		origData=[{'<dd><a href="http://www.renren.com/profile.do?id=266754031">王瑛</a>', '<dd><a href="http://www.renren.com/profile.do?id=27331442">Ethan.王哲</a>', '<dd><a href="http://www.renren.com/profile.do?id=240303471">刘洋English</a>'},{'<dd><a href="http://www.renren.com/profile.do?id=239439171"></a>','<dd><a href="http://www.renren.com/profile.do?id=222439171">eeee</a>'},{'<dd><a href="http://www.renren.com/profile.do?id=324134134">～！@#￥%……&*（）</a>'},{}]
		exptData=[{'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English'},{'239439171':'','222439171':'eeee'},{'324134134':'～！@#￥%……&*（）'},{}]
		for i in range(0,len(origData)):#several friendList to parser
			self.assertEquals(self.parser.friendList(origData[i]),exptData[i])
	def testProfileLocal(self):
		renrenId='32324'
		path='./renrenData/testData'
		for file in os.listdir(path):
			f=open(path+'/'+file,'r')
			htmlStr=str(f.readlines())
			self.parser.profile(renrenId,htmlStr)
	def testProfile(self):
		renrenIds={'233330059','241331952'}
		#tag only, few values
		#renrenId='285060168'#no info
		#renrenId='241331952'#company info 
		#renrenId='285060168'#unavailable
		#renrenId='223981104'#timeline unavailable
		browser=RenrenBrowser()
		browser.login()
		for renrenId in renrenIds:
			htmlStr=browser.profile(renrenId)
			self.parser.profile(renrenId,htmlStr)
		self.data.out()

if __name__=='__main__':
	suite=unittest.TestSuite()
	suite.addTest(TestRenrenParser('testFriendList'))
	#suite.addTest(TestRenrenParser('testProfile'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
