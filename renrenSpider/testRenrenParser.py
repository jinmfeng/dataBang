from renrenBrowser import *
from renrenParser import *
from renrenCache import *

renrenIds=('233330059','254786440','227259740')#uavailable
renrenIds=('233330059','241331952')#uavailable

browser=RenrenBrowser()
browser.login()
browser.setLogLevel(20)

data=RenrenCache()
parser=RenrenParser(data)

for renrenId in renrenIds:
	#flist=browser.friendList(renrenId)
	#parser.friends(renrenId,flist)
	htmlStr=browser.profile(renrenId)
	browser.savePage('profile',htmlStr)
	parser.profile(renrenId,htmlStr)

#data.out()

#print(browser.status(renrenId))
