import unittest
import os

from renrenParser import *
from renrenCache import *
from renrenBrowser import *

class TestRenrenParser(unittest.TestCase):

	def setUp(self):
		self.data=RenrenCache()
		self.parser=RenrenParser(self.data)

	def tearDown(self):
#		self.browser.dispose()
		self.parser=None

	def testFriendList(self):
		#test data
		flist=[{'<dd><a href="http://www.renren.com/profile.do?id=266754031">王瑛</a>', '<dd><a href="http://www.renren.com/profile.do?id=27331442">Ethan.王哲</a>', '<dd><a href="http://www.renren.com/profile.do?id=240303471">刘洋English</a>'},{'<dd><a href="http://www.renren.com/profile.do?id=239439171"></a>','<dd><a href="http://www.renren.com/profile.do?id=222439171">eeee</a>'},{'<dd><a href="http://www.renren.com/profile.do?id=324134134">～！@#￥%……&*（）</a>'},{}]
		renrenId=['111111','22222','33333','44444']
		names=[{'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English'},{'239439171':'','222439171':'eeee'},{'324134134':'～！@#￥%……&*（）'},{}]
		expFl=dict()
		expName=dict()
		for i in range(0,len(renrenId)):#several friendList to parser
			expFl[renrenId[i]]=set(names[i].keys())
			expName.update(names[i])
			self.parser.friendList(renrenId[i],flist[i])
		self.assertEquals(self.data.getAttrData('friendList'),expFl)
		self.assertEquals(self.data.getAttrData('name'),expName)
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
	suite.addTest(TestRenrenParser('testProfile'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
