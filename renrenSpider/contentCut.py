import renrenDb
import jieba

db=renrenDb.RenrenDb()
conn=db.getConn()
cur=conn.cursor()
#renrenId='410941086'
renrenId='427674621'
#renrenId='233330059'
sql="select content from temp_status where renrenId={}".format(renrenId)
cur.execute(sql)

tags=dict()
#key-tag, value-frequence
for content in cur.fetchall():
	seg=jieba.cut(content[0],cut_all=False)
	for item in seg:
		if item in tags.keys():
			tags[item]=tags[item]+1
		else:
			tags[item]=1
cur.close()
conn.close()

freq=dict()
#key-renrenId, value-frequence
for tt in tags.items():
	if (str.isdigit(tt[0].encode('utf-8'))) and ( tt[1]>3):
		freq[tt[0].encode('utf-8')]=tt[1]
aa=sorted(freq.items(), key=lambda d: d[1],reverse=True)

#show frequence, renrenId, name
names=db.getNames(freq.keys())
for item in aa:
	try:
		print(str(item[1]).ljust(5)+item[0]+'  '+names[item[0]])
	except Exception as e:
		pass
