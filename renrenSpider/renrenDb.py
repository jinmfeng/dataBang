import pymysql

class RenrenDb:
	
	renren_relation='t_renren_relation'
	temp_relation='temp_relation'
	renren_detail_profile='t_renren_detail_profile'
	temp_detail_profile='temp_detail_profile'
	renren_name='t_renren_name'
	temp_name='temp_name'

	detailCol={'生日':'birth','星座':'star','家乡':'hometown','等级':'rrlvl','性别':'gender','大学':'school_college','高中':'school_senior','中专技校':'school_tech','初中':'school_junior','小学':'school_primary','公司':'company','时间':'time','QQ':'qq','MSN':'msn','手机号':'phone','个人网站':'personal_website','我的域名':'domain1','个性域名':'domain2'}
	def __init__(self):
		pass

	def createTable(self):
		pass

	def getConn(self,db='data_bang'):
		return pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Kunth123',db=db,charset='utf8')
	def execute(self,sql=None):
		conn=self.getConn()
		cur=conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
		conn.close()

	def deleteRelation(col,renrenId,table='net_renren'):
		conn=getConn()
		cur=conn.cursor()
		n=cur.execute("delete from FROM {} where renrenId{}={}".format(table,str(col),renrenId))
		cur.commit()
		cur.close()
		conn.close()
		return n 

	def getRenrenId(self,col,renrenId):
		conn=self.getConn()
		cur=conn.cursor()
		target=str(col)
		where=str(col%2+1)
		res=set()
		for table in [self.renren_relation,self.temp_relation]:
			cur.execute("SELECT renrenId{} FROM {} where renrenId{}={}".format(target,table,where,renrenId))
			for item in cur.fetchall():
				res.add(item[0])
		cur.close()
		conn.close()
		return list(res)

	def getSearched(self):
		conn=self.getConn()
		cur=conn.cursor()
		res=set()
		table=self.renren_relation
		cur.execute("SELECT renrenId1 FROM {} group by renrenId1".format(table))
		for item in cur.fetchall():
			res.add(item[0])
		cur.close()
		conn.close()
		return list(res)
	def getName(self,renrenId):
		conn=self.getConn()
		cur=conn.cursor()

		name=''
		for table in [self.renren_name,self.temp_name]:
			n=cur.execute('select name from {} where renrenId={}'.format(table,renrenId))
			if n>0:
				name=cur.fetchall()[0][0]
		cur.close()
		conn.close()
		return name
	def getNames(self,renrenIds):
		conn=self.getConn()
		cur=conn.cursor()

		names=dict()
		for table in [self.renren_name,self.temp_name]:
			cur.execute('select renrenId,name from {} where renrenId in ({})'.format(table,str(renrenIds).strip('[]{}')))
			for item in cur.fetchall():
				names[item[0]]=item[1]
		cur.close()
		conn.close()
		return names

	def getRelations(self,ids):
		conn=self.getConn()
		cur=conn.cursor()
		ids=set(ids)
		sql2="select renrenId1,renrenId2 from t_renren_relation where renrenId1 in ({}) and renrenId2 in({})"
		cur.execute(sql2.format(str(ids).strip('{}'),str(ids).strip('[]{}')))
		edge=cur.fetchall()
		cur.close()
		conn.close()
		return edge

	def insertFriendList(self,renrenId,friendList):
		#construct sql, insert into table (col1, col2) values (v11,v12),(v21,v22)
		sql='insert into '+self.temp_relation+' (renrenId1,renrenId2) values '
		for friend in friendList:
			sql=sql+'({},{}),'.format(renrenId,friend)
		self.execute(sql.rstrip(','))
	def insertName(self,name):
		sql='insert into '+self.temp_name+' (renrenId,name) values '
		for item in name.items():
			sql=sql+str(item)+','
		self.execute(sql.rstrip(','))
	def insertProfile(self,renrenId,profile):
		sql='insert into '+self.temp_detail_profile+' set renrenId={},'.format(renrenId)
		for item in profile.items():
			sql=sql+self.detailCol[item[0]]+"='"+item[1]+"',"
		self.execute(sql.rstrip(','))
