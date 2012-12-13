import renrenDb

db=renrenDb.RenrenDb()
conn=db.getConn()
cur=conn.cursor()
cur.execute('select content from t_renren_status')
f=open('head.txt','w')
last=''
for item in cur.fetchall():
	idx=item[0].find("</a>:",100)
	if last==item[0][0:idx+5]:
		pass
	else:
		last=item[0][0:idx+5]
		f.write(item[0][0:idx+5]+'\n')
f.close()
cur.close()
conn.close()
