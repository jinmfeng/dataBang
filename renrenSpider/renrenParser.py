import re
import time
import os

class RenrenParser:
	def __init__(self):
		pass

	def friendList(self,items):
		name=dict()
		ptn=re.compile(r'id=(\d+)">([^<]*?)</a>')
		for item in items:
			m=ptn.search(item)
			if m == None:#parse error, return
				return -1 
			name[m.group(1)]=m.group(2)
		return name
	def profile(self,page):
		#parser out all <dt>tag</dt>\W*?<dd>value</dd>
		itemPtn=r'<dt>[^<]*?</dt>[^<]*?<dd>.*?</dd>'
		items=re.compile(itemPtn,re.DOTALL).findall(page)
		ptn=re.compile(r'<dt>(.*?)</dt>[^<]*?<dd>(.*?)</dd>',re.DOTALL)
		profile=dict()
		for item in items:
			pair=ptn.search(item)
			if pair.group(1).find('所在')==0:continue #duplicated info
			if pair.group(2).find('pf_birth')!=-1:continue #duplicated item, drop
			value=re.sub(r'<a\s[^>]+?>([^<]*?)</a>',r'\1',pair.group(2))#drop link
			value=re.sub(r'(?:&nbsp;)|(?:\"\+response\.[a-z]+\+\")|\s+',r'',value)
			if value=='':
				continue
			else:
				tag=re.sub(r'\s+|:',r'',pair.group(1))
				profile[tag]=value
		return profile
