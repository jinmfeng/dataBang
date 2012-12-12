#coding=utf-8

import renrenDb
import time
import numpy as np
import matplotlib.pyplot as plt

db=renrenDb.RenrenDb()
#renrenId='233330059'
renrenId='410941086'
sql="SELECT timestamp FROM temp_status where renrenId={}".format(renrenId)
conn=db.getConn()
cur=conn.cursor()
n=cur.execute(sql)
sec=[]
for item in cur.fetchall():
	sec.append(time.mktime(time.strptime(item[0],'%Y-%m-%d %H:%M')))

a=np.float64(sec)
#print(len(a))
mina=min(a)
delta=24*60*60*30
weeks=(max(a)-mina)/delta
y=np.zeros(weeks+1)
idx=(a-mina)/delta

for i in idx:
	try:
		y[int(i)]=y[int(i)]+1
	except Exception as e:
		print(i)

plt.plot(y)
plt.ylabel('num of status')
plt.xlabel('months')
title='Zhang Xiaoxu'
#title='Yang Jiekun'
plt.title(title)
plt.grid()
plt.show()
