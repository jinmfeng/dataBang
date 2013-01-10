from renrenBrowser import *
from renrenParser import *
from renrenCache import *

renrenIds=('233330059','254786440','227259740')#uavailable

browser=RenrenBrowser()
browser.login()
browser.setLogLevel(20)

data=RenrenCache()
parser=RenrenParser(data)

for renrenId in renrenIds:
	flist=browser.friendList(renrenId)
	parser.friends(renrenId,flist)

data.out()

#print(browser.status(renrenId))
