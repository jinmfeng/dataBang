import pickle
import os

class RenrenCache:
	dataFileTmplt="{}/{}.p"#path,attrName
	def __init__(self,path='./renrenData/objs'):
		self.path=path
		self.data=dict()
		self.initAttr()
	def __del__(self):
		pass

	def load(self,path=None):
		if path==None:
			path=self.path
		for attr in self.data.keys():
			try:
				self.data[attr]=pickle.load(open(self.dataFileTmplt.format(path,attr),'rb'))
			except Exception as e:
				self.data[attr]=dict()#duplicate
	def save(self,path=None):
		if path==None:
			path=self.path
		if os.path.exists(path)==False:
			os.makedirs(path)
		for item in self.data.items():
			pickle.dump(item[1],open(self.dataFileTmplt.format(path,item[0]),'wb'))

	def out(self):
		print('attrs list: {}'.format(self.data.keys()))
		for item in self.data.items():
			#print('{}:{}'.format(item[0],item[1]))
			print('{}:{} items'.format(item[0],len(item[1])))

	def addItem(self,attr,renrenId,value):
		#override
		if attr not in self.data.keys():
			self.addAttr(attr)
		self.data[attr][renrenId]=value
	def addItems(self,attr,keyValue):
		#override
		if attr not in self.data.keys():
			self.addAttr(attr)
		self.data[attr].update(keyValue)

	def getValue(self,attr,renrenId):
		return self.data[attr][renrenId]
	def getAttrData(self,attr):
		return self.data[attr]

	def initAttr(self,attrs={'friendList','name'}):
		self.clear()
		if type(attrs)!=type(set()):
			print('input error, expect: type(attrs)=set()')
		for attr in attrs:
			self.data[attr]=dict()
	def addAttr(self,attr):
		if attr not in self.data.keys():
			self.data[attr]=dict()
	def getAttrs(self):
		return set(self.data.keys())

	def clear(self):
		self.data=dict()
		#for attr in self.data.keys():
			#self.data[attr]=dict()
