import pymysql

class RenrenDb:
	renren_relation='t_renren_relation'
	temp_relation='temp_relation'
	renren_detail_profile='t_renren_detail_profile'
	temp_detail_profile='temp_detail_profile'
	renren_name='t_renren_name'
	temp_name='temp_name'
	sqls=dict()
	sqls['name']='CREATE TABLE if not exists {} (renrenId varchar(15) NOT NULL,name varchar(20){})ENGINE=InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_unicode_ci;'
	sqls['relation']='CREATE TABLE if not exists {} (renrenId1 varchar(15) NOT NULL,renrenId2 varchar(15) NOT NULL,KEY one(renrenId1),KEY two(renrenId2) {})ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_unicode_ci;'
	sqls['profile']='CREATE TABLE if not exists {} (renrenId varchar(20) NOT NULL,school_college varchar(50),school_senior varchar(50),school_junior varchar(50),school_primary varchar(50),school_tech varchar(50),birth varchar(20),star varchar(10),gender varchar(10),rrlvl varchar(5),phone varchar(20),qq varchar(15),msn varchar(50),personal_website varchar(50),hometown varchar(50),company varchar(50),time varchar(50),domain1 varchar(50),domain2 varchar(50) {})ENGINE=InnoDB DEFAULT CHARSET = utf8;'

	detailCol={'生日':'birth','星座':'star','家乡':'hometown','等级':'rrlvl','性别':'gender','大学':'school_college','高中':'school_senior','中专技校':'school_tech','初中':'school_junior','小学':'school_primary','公司':'company','时间':'time','QQ':'qq','MSN':'msn','手机号':'phone','个人网站':'personal_website','我的域名':'domain1','个性域名':'domain2'}
	def __init__(self,namePre='test'):
		self.info={'relation','name','profile'}
		self.mainTable=dict()
		self.tempTable=dict()
		for table in self.info: 
			self.mainTable[table]='{}_main_{}'.format(namePre,table)
			self.tempTable[table]='{}_temp_{}'.format(namePre,table)

	def createTempTable(self):
		key={'name':',KEY idx_temp(renrenId)','relation':',KEY idx_temp (renrenId1,renrenId2)','profile':',KEY (renrenId)'}
		sql=set()
		for attr in self.sqls.keys():
			tableName=self.tempTable[attr]
			sql.add(self.sqls[attr].format(tableName,key[attr]))
		n=self.execute(sql)
		return n
	def createMainTable(self):
		primary={'name':',PRIMARY KEY (renrenId)','profile':',PRIMARY KEY (renrenId)','relation':',PRIMARY KEY (renrenId1,renrenId2)'}
		sql=set()
		for attr in self.sqls.keys():
			tableName=self.mainTable[attr]
			sql.add(self.sqls[attr].format(tableName,primary[attr]))
		n=self.execute(sql)
		return n
	def dropTempTable(self):
		sqls=set()
		for table in self.tempTable.values():
			sqls.add('drop table if exists {}'.format(table))
		self.execute(sqls)
	def dropMainTable(self):
		sqls=set()
		for table in self.mainTable.values():
			sqls.add('drop table if exists {}'.format(table))
		self.execute(sqls)

	def getConn(self,db='data_bang'):
		return pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Kunth123',db=db,charset='utf8')
	def execute(self,sql=None):
		conn=self.getConn()
		cur=conn.cursor()
		if type(sql) == type(''):
			n=cur.execute(sql)
		else:
			n=0
			for sql1 in sql:
				n=n+cur.execute(sql1)
		conn.commit()
		cur.close()
		conn.close()
		return n

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
		for table in [self.mainTable['relation'],self.tempTable['relation']]:
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
		for table in [self.mainTable['relation'],self.tempTable['relation']]:
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
		sql='insert into '+self.tempTable['relation']+' (renrenId1,renrenId2) values '
		for friend in friendList:
			sql=sql+'({},{}),'.format(renrenId,friend)
		self.execute(sql.rstrip(','))
	def insertName(self,name):
		sql='insert into '+self.tempTable['name']+' (renrenId,name) values '
		for item in name.items():
			sql=sql+str(item)+','
		self.execute(sql.rstrip(','))
	def insertProfile(self,renrenId,profile):
		sql='insert into '+self.tempTable['profile']+' set renrenId={},'.format(renrenId)
		for item in profile.items():
			sql=sql+self.detailCol[item[0]]+"='"+item[1]+"',"
		self.execute(sql.rstrip(','))
