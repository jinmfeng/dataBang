import pickle
import os

class RenrenCache:
	dataFileTmplt="{}/{}.p"#path,attrName
	def __init__(self,path='.'):
		self.attrs={'friends':dict(),'name':dict()}
		self.load()
	def __del__(self):
		pass

	def load(self,path='./renrenData/dict'):
		for attr in self.attrs.keys():
			try:
				self.attrs[attr]=pickle.load(open(self.dataFileTmplt.format(path,attr),'rb'))
				#print("{} ok".format(attr))#log
			except Exception as e:
				self.attrs[attr]={}
				#print("{} fail".format(attr))#log
	def save(self,path='./renrenData/dict'):
		if os.path.exists(path)==False:
			os.makedirs(path)
		#self.attrsFile=path+'/attrs.p'
		#pickle.dump(self.attrs,open(self.attrsFile,'wb'))
		for item in self.attrs.items():
			pickle.dump(item[1],open(self.dataFileTmplt.format(path,item[0]),'wb'))

	def out(self):
		print('attrs list: {}'.format(self.attrs.keys()))
		for item in self.attrs.values():
			print('{}:{}'.format(item[0],item[1]))

	def addItem(self,attr,renrenId,value):
		#override
		self.attrs[attr][renrenId]=value
	def addItems(self,attr,keyValue):
		#override
		self.attrs[attr].update(keyValue)
