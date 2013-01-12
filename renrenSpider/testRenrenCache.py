import unittest

from renrenCache import *

class TestRenrenCache(unittest.TestCase):

	def setUp(self):
		self.data=RenrenCache()
		self.attrs={'junior','大学','高中senior',''}
		self.initAttr={'friendList','name'}
	def tearDown(self):
		self.data=None

	def testAttr(self):
		#right after declared, attr=init, {'friendList','name'}
		self.assertEquals(self.data.getAttrs(),self.initAttr)
		#attr not exist, insert and value=dict()
		expAttr=self.initAttr
		for attr in self.attrs:
			self.data.addAttr(attr)
			expAttr.add(attr)
			self.assertEquals(self.data.getAttrs(),expAttr)
			self.assertEquals(self.data.getAttrData(attr),dict())
		#attr exist, insert and nothing changed.
		#more test
	def testAdd(self):
		toAdd={'23424':'yang','5345345':'w杨ng','4444':'杨'}
		modified={'23424':'wang','34234':'w杨ng','4444':'杨'}
		#add 1 item each time, attr exist
		for item in toAdd.keys():
			self.data.addItem('name',item,toAdd[item])
			self.assertEquals(self.data.getValue('name',item),toAdd[item])
		self.assertEquals(self.data.getAttrData('name'),toAdd)
		#add 1 item each time, attr not exist
		for item in toAdd.keys():
			self.data.addItem('tag',item,toAdd[item])
			self.assertEquals(self.data.getValue('tag',item),toAdd[item])
		self.assertEquals(self.data.getAttrData('tag'),toAdd)
		#add several items, attr exist
		self.data.addItems('friendList',toAdd)
		self.assertEquals(self.data.getAttrData('friendList'),toAdd)
		#add several items, attr not exist
		self.data.addItems('vivian',toAdd)
		self.assertEquals(self.data.getAttrData('vivian'),toAdd)
		#add dupilicate, override.
		for item in modified.keys():
			self.data.addItem('name',item,modified[item])
			self.assertEquals(self.data.getValue('name',item),modified[item])
		toAdd.update(modified)
		self.assertEquals(self.data.getAttrData('name'),toAdd)
	def testAddExistAttr(self):
		toAdd={'23424':'yang','5345345':'w杨ng','4444':'杨'}
		self.data.addItems('attr',toAdd)
		oldAttr=self.data.getAttrs()
		self.data.addAttr('attr')
		self.assertEquals(self.data.getAttrs(),oldAttr)
		self.assertEquals(self.data.getAttrData('attr'),toAdd)
	def testClear(self):
		self.data.clear()
		self.assertEquals(self.data.getAttrs(),set())

if __name__=='__main__':
	suite=unittest.TestSuite()
	suite.addTest(TestRenrenCache('testAttr'))
	suite.addTest(TestRenrenCache('testAdd'))
	suite.addTest(TestRenrenCache('testAddExistAttr'))
	suite.addTest(TestRenrenCache('testClear'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
