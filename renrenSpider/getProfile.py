import renrenBrowser
import renrenDb
import renrenParser
import time

class RenrenProfile():
	def __init__(self,tablePre='orig'):
		self.parser=renrenParser.RenrenParser()
		self.db=renrenDb.RenrenDb(tablePre)
		self.browser=renrenBrowser.RenrenBrowser()
		self.browser.setLogLevel(20)
		self.browser.login()
		
		self.searched=self.db.getSearched('profile')

	def get(self,renrenId):
		target=self.db.getRenrenId(2,renrenId)
		toSearch=target-self.searched
		cnt=0
		for renrenId in toSearch:
			pf=self.parser.profile(self.browser.profile(renrenId))
			self.db.insertProfile(renrenId,pf)
			cnt += 1
			if pf!=dict():
				print(cnt)
				time.sleep(10)
			else:
				print('empty')

if __name__=='__main__':
	pf=RenrenProfile()
	pf.get('233330059')
	
