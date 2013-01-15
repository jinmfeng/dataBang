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
		origData=[{'<dd><a href="http://www.renren.com/profile.do?id=266754031">王瑛</a>', '<dd><a href="http://www.renren.com/profile.do?id=27331442">Ethan.王哲</a>', '<dd><a href="http://www.renren.com/profile.do?id=240303471">刘洋English</a>'},{'<dd><a href="http://www.renren.com/profile.do?id=239439171"></a>','<dd><a href="http://www.renren.com/profile.do?id=222439171">eeee</a>'},{'<dd><a href="http://www.renren.com/profile.do?id=324134134">～！@#￥%……&*（）</a>'},{},{'error'}]
		exptData=[{'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English'},{'239439171':'','222439171':'eeee'},{'324134134':'～！@#￥%……&*（）'},{},-1]
		for i in range(0,len(origData)):#several friendList to parser
			self.assertEquals(self.parser.friendList(origData[i]),exptData[i])
	def testProfileLocal(self):#some codesc problem with local file reading
		path='./renrenData/testData'
		for file in os.listdir(path):
			f=open(path+'/'+file,'rb')
			htmlStr=str(f.readlines())
			print(htmlStr.decode("UTF-8"))
			#self.parser.profile(htmlStr)
	def testProfile(self):
		renrenIds=['233330059','241331952','294126602','230760442','239486743','285060168','223981104']#basic, timeLine
		isEmpty=[False,False,False,False,False,True,True]
		browser=RenrenBrowser()
		for i in range(0,len(renrenIds)):
			htmlStr=browser.profile(renrenIds[i])
			#self.assertEquals(self.parser.profile(htmlStr)==dict(),isEmpty[i])
			print(self.parser.profile(htmlStr))
		#print('testProfile need to check manually')

if __name__=='__main__':
	suite=unittest.TestSuite()
	#suite.addTest(TestRenrenParser('testFriendList'))
	suite.addTest(TestRenrenParser('testProfile'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
