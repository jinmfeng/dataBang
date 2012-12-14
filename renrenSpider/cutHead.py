import renrenDb
import re

db=renrenDb.RenrenDb()
conn=db.getConn()
cur=conn.cursor()
cur.execute('select content from orig_renren_status')
f=open('head.txt','w')
last1=''
last2=''
for item in cur.fetchall():
	#cut head
	noHead=''
	idx=item[0].find("</a>:",100)
	noHead=item[0][idx+5:]

	#img emotion and icon
	imgPtn=r"<img\s+src=\W+http://a.xnimg.cn/imgpro/.+?/>"
	imgs=re.compile(imgPtn).findall(noHead)
	for img in imgs:
		#f.write(img+'\n')#check result
		noHead=noHead.replace(img,' renrenEmotion ')

	#forward status
	forwardPtn='\u8f6c\u81ea<a\s+href.*?>'
	m=re.compile(forwardPtn).search(noHead)
	if m!=None:
		noHead=noHead[:m.end()]
		selfProfPtn=r'(?P<prof><a\s+href=\W*http://www.renren.com/profile.do\?id=(?P<id>\d+).*?>)'
		publicProfPtn=r'(?P<prof><a\s+href=\W*http://page.renren.com/(?P<id>\d+).*?>)'
		selfProf=re.compile(selfProfPtn).search(noHead)
		publicProf=re.compile(publicProfPtn).search(noHead)
		if selfProf!=None:
			#if last1==len(selfProf.group('prof')):
				#pass
			#else:
				#last1=len(selfProf.group('prof'))
				#f.write(selfProf.group('prof')+'\n')#check result
			noHead=noHead.replace('\u8f6c\u81ea'+selfProf.group('prof'),' forword_{} '.format(selfProf.group('id')))
		if publicProf!=None:
			#if last2==len(publicProf.group('prof')):
				#pass
			#else:
				#last2=len(publicProf.group('prof'))
				#f.write(publicProf.group('prof')+'\n')#check result
			noHead=noHead.replace('\u8f6c\u81ea'+publicProf.group('prof'),' forword_{} '.format(publicProf.group('id')))

	#multi at item
	atItemPtn=r"<a\s+href=\W*http://www.renren.com/g/\d+.*?>@.*?</a>"
	atPtn=r"<a\s+href=\W*http://www.renren.com/g/(?P<id>\d+).*?>@.*?</a>"
	atItem=re.compile(atItemPtn).findall(noHead)
	for item in atItem:
		m=re.compile(atPtn).search(item)
		#if last2==len(m.group('at')):
			#pass
		#else:
			#last2=len(m.group('at'))
			#f.write(m.group('at')+'\n')#check result
		noHead=noHead.replace(item,' at_{} '.format(m.group('id')))

	#cut end
	endStr="\\n\', \'"
	if noHead.endswith(endStr):
		idx=noHead.rindex(endStr)
	print(noHead[:idx])
	#print(noHead)

f.close()
cur.close()
conn.close()
