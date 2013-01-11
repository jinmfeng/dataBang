import shutil
import os
import unittest

from renrenBrowser import *

class TestRenrenBrowser(unittest.TestCase):

	def setUp(self):
		self.pwdRoot='./testBrowser'
		self.pwdSave=self.pwdRoot+'/renrenData/pages'
		if os.path.exists(self.pwdSave)==True:
			shutil.rmtree(self.pwdSave)

		self.browser=RenrenBrowser(path=self.pwdRoot)
		self.browser.login()

	def tearDown(self):
#		self.browser.dispose()
		self.browser=None
		pass

	def testProfile(self):
		renrenIds={'233330059','230760442','223981104','410941086','285060168'}
							#myself,timeline ok/unavailable,old style ok/unavailable
		self.browser.setLogLevel(10)#debug

		self.browser.localSave(False)
		for renrenId in renrenIds:
			self.assertNotEqual(self.browser.profile(renrenId),'timeout')
		self.assertFalse(os.path.exists(self.pwdSave))#path not exist

		self.browser.localSave(True)
		for renrenId in renrenIds:
			self.assertNotEqual(self.browser.profile(renrenId),'timeout')
		self.assertEqual(len(os.listdir(self.pwdSave)),len(renrenIds))

	def testFriendList(self):
		#page style: ok/unavailable
		#number of total pages: 0,1,more
		#curpage of curpage requesting

#target 1 page and check htmlStr not 'timeout'
		renrenIds={'233330059','410941086','267654044','285060168','240303471'}
							#myself,3+pages/2pages/1page/unavailable
		self.browser.setLogLevel(10)#debug
		#target page=0,1,2,3
		self.browser.localSave(False)
		for targetPage in range(0,3):
			for renrenId in renrenIds:
				self.assertNotEqual(self.browser.friendList(renrenId,targetPage),'timeout')
			self.assertFalse(os.path.exists(self.pwdSave))#path not exist
		self.browser.localSave(True)
		for targetPage in range(0,3):
			for renrenId in renrenIds:
				self.assertNotEqual(self.browser.friendList(renrenId,targetPage),'timeout')
			self.assertEqual(len(os.listdir(self.pwdSave)),len(renrenIds)*(targetPage+1))

		#target all pages and check len(set)
		flist={'232639310':35,'242543024':152,'285060168':4}
		for item in flist.items():
			self.assertEqual(len(self.browser.friendList(item[0])),item[1])

if __name__=='__main__':
	suite=unittest.TestSuite()
	suite.addTest(TestRenrenBrowser('testProfile'))
	suite.addTest(TestRenrenBrowser('testFriendList'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
