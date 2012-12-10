from renrenBrowser import *
from renrenParser import *
from renrenDb import *

parser=RenrenParser()
db=RenrenDb()

browser=RenrenBrowser()
browser.setLogLevel(40)
browser.login()

orig='233330059'

#net1 and my profile
#browser.friendPage(orig)
#browser.profilePage(orig)
#parser.friends()

#flag=input('continue net2?(Y/N)')

#net2 and friends profile
#flist=db.getRenrenId(2,orig)
#for item in flist:
	#loopStart=time.time()
	#browser.friendPage(item)
	#loopEnd=time.time()
	#if (loopEnd-loopStart<10):
		#print('loop time={},parsering to kill time'.format(loopEnd-loopStart))
		#parser.friends()
		#kill=time.time()
		#print('time cost ={}'.format(kill-loopEnd))
	#browser.profilePage(item)
#parser.friends()

#net3 friend page only
searched=set(db.getSearched())
#net2 list 
flist=db.getRenrenId(2,orig)
conn=db.getConn()
cur=conn.cursor()
cur.execute('select renrenId from myFriend where seq={}'.format(4))
flist=[]
for item in cur.fetchall():
	flist.append(item[0])
flist=[]
for myFriend in flist:
	ff=set(db.getRenrenId(2,myFriend))
	toSearch=ff-searched
	print('begin to get net2 of {}, name={}, toSearch {}/{}'.format(myFriend,db.getName(myFriend),len(toSearch),len(ff)))
	loop21=time.time()
	for i,item in zip(range(0,len(toSearch)),toSearch):
		if (i%20)==1:
			pause=time.time()
			timestamp=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
			print('{}, {}/{} is done,time cost={}'.format(timestamp,i,len(toSearch),pause-loop21))
		browser.friendPage(item)
	searched=searched | toSearch
	loop22=time.time()
	print('net2 of {} searched, time cost={}'.format(myFriend,loop22-loop21))
parser.friends()
