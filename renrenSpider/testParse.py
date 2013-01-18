import unittest
import rparse

pfHrefs=[
	{'<dd><a href="http://www.renren.com/profile.do?id=6754031">王瑛</a>',
	'<dd><a href="http://www.renren.com/profile.do?id=331442">En.王哲</a>'},
	{'<dd><a href="http://www.renren.com/profile.do?id=9439171"></a>'},
	'<dd><a href="http://www.renren.com/profile.do?id=34134">～@%……</a>',
	{'error'}]
names=[
	{'6754031':'王瑛','331442':'En.王哲'},
	{'9439171':''},
	{'34134':'～@%……'},
	None]

class TestRenrenParser(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass
#		self.browser.dispose()

	def testFriendList(self):
		#pfHrefs=self.pfHrefs
		#names=self.names
		for pfHref,name in zip(pfHrefs,names):
			self.assertEquals(rparse.friendList(pfHref),name)
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
	suite.addTest(TestRenrenParser('testFriendList'))
	#suite.addTest(TestRenrenParser('testProfile'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
