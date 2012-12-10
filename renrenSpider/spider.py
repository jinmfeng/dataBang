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
#flist=db.getRenrenId(2,orig)
#seq 1 vip
#flist=['410941086','284874220','427674621','405228416','439682367','453367603','471565324','472854825']
#seq 2
#flist=["200111024","229416854","229609670","229877878","229908293","229939633","230062380","230628865","230760442","230760675","230801687","232279547","232411002","233528843","234770082","234880437","235445327","236602271","236939419","237731470","238347326","238733506","239309951","239663011","240218881","242843921","250798745","259758954","267776987","269911290","268352861",'261362789']
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
