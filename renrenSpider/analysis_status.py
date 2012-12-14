import renrenDb
import re

db=renrenDb.RenrenDb()
conn=db.getConn()
cur=conn.cursor()
cur.execute('select content,statusId,renrenId from orig_renren_status')

forword=dict()#statusId:sourceRenrenId
at=dict()#statusId:atRenrenIdList:
freq=dict()#renrenId:freqDict.  freqDict----renrenId:freq
for item in cur.fetchall():
	statusId=item[1]
	renrenId=item[2]
	#cut head
	content=''
	idx=item[0].find("</a>:",100)
	content=item[0][idx+5:]

	#img emotion and icon
	imgPtn=r"<img\s+src=\W+http://a.xnimg.cn/imgpro/.+?/>"
	imgs=re.compile(imgPtn).findall(content)
	for img in imgs:
		content=content.replace(img,' renrenEmotion ')

	#forward status and endStr
	forwardPtn='\u8f6c\u81ea<a\s+href=\W*http://.+?(?P<id>\d+).*?>'
	m=re.compile(forwardPtn).search(content)
	if m!=None:
		content=content[:m.start()]+' forword_{} '.format(m.group('id'))
		forword[statusId]=m.group('id')
	else:
		forword[statusId]='0'
		endStr=["\\n\', \'","\\n\", \'"]
		for ends in endStr:
			idx=content.rfind(ends)
			if(idx!=-1):
				break
		content=content[:idx]

	#multi at item
	atItemPtn=r"<a\s+href=\W*http://www.renren.com/g/\d+.*?>@.*?</a>"
	atPtn=r"<a\s+href=\W*http://www.renren.com/g/(?P<id>\d+).*?>@.*?</a>"
	atlist=[]
	if renrenId not in freq.keys():
		freq[renrenId]=dict()
	atItems=re.compile(atItemPtn).findall(content)
	for item in atItems:
		m=re.compile(atPtn).search(item)
		atedId=m.group('id')
		content=content.replace(item,' at_{} '.format(atedId))
		atlist.append(atedId)
		#update freq info with atedId
		if atedId in freq[renrenId].keys():
			freq[renrenId][atedId]=freq[renrenId][atedId]+1
		else:
			freq[renrenId][atedId]=1
		#print(freq[renrenId])
	if len(atlist)>0:
		at[statusId]=atlist

	#print(content)
#print(forword)
#print(at)
#print(freq)
names=db.getNames(list(freq.keys()))
f=open('atFreq.txt','w')
for (uid,ifreq) in freq.items():
	if len(ifreq)<1:
		#print(names[uid])
		continue
	f.write(names[uid]+'\n')
	subnames=db.getNames(list(ifreq.keys()))
	aa=sorted(ifreq.items(), key=lambda d: d[1],reverse=True)
	for fitem in aa:
		try:
			name=subnames[fitem[0]]
		except:
			#name=db.getName(fitem[0])
			name='帐号未录入数据库，注销'
			print(fitem[0])
		f.write('  '+str(fitem[1]).ljust(5)+fitem[0]+'  '+name+'\n')
	f.write('\n')

cur.close()
conn.close()
f.close()
