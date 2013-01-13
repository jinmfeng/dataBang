import unittest

from renrenDb import *
from renrenParser import *

class TestRenrenDb(unittest.TestCase):

	def setUp(self):
		self.db=RenrenDb()

	def tearDown(self):
#		self.browser.dispose()
		self.db=None

	def testInsertFriendList(self):
		name={'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'}
		self.db.insertFriendList('11111',set(name.keys()))
	def testInsertName(self):
		name={'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'}
		self.db.insertName(name)
	def testInsertProfile(self):
		profiles=[{'家乡': '山东青岛市', '高中': '山东省平度第九中学-2004年', '大学': '西安建筑科大-2007年-管理学院<br>', '时间': '2011年-7月至现在', '公司': '大亚湾核电运营管理有限责任公司', '初中': '杭州路中学-2001年', '星座': '金牛座', '生日': '1988-5-9', '性别': '男', '等级': '26级'},{'家乡': '安徽巢湖市', '我的域名': 'zmoony.renren.com', '小学': '成都实验小学-1996年', '高中': '四川省成都市第七中学-2005年', '大学': '清华大学-2008年-计算机科学与技术系<br>清华大学-2012年-交叉信息研究院<br>', '个性域名': 'zmoony.renren.com', '初中': '七中育才中学-2002年', '星座': '双鱼座', '生日': '1990-3-20', '性别': '男', '等级': '40级'},{'QQ': '309097050', '家乡': '内蒙古呼伦贝尔市', '手机号': '15191895258', '星座': '水瓶座', '生日': '1998-2-13', '性别': '男', '等级': '22级'}]
		renrenIds=['1111111','222222','33333333']
		for (renrenId,profile) in zip(renrenIds,profiles):
			self.db.insertProfile(renrenId,profile)

if __name__=='__main__':
	suite=unittest.TestSuite()
	suite.addTest(TestRenrenDb('testInsertFriendList'))
	suite.addTest(TestRenrenDb('testInsertName'))
	suite.addTest(TestRenrenDb('testInsertProfile'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
