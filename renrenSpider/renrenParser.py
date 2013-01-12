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
				return item
			name[m.group(1)]=m.group(2)
		return name

	def profile(self,renrenId,page):
		#parser out all <dt>tag</dt>\W*?<dd>value</dd>
		itemPtn=r'<dt>[^<]*?</dt>[^<]*?<dd>.*?</dd>'
		items=re.compile(itemPtn,re.DOTALL).findall(page)
		ptn=re.compile(r'<dt>(.*?)</dt>[^<]*?<dd>(.*?)</dd>',re.DOTALL)
		for item in items:
			pair=ptn.search(item)
			try:
				tag=pair.group(1).strip('\n')
				value=pair.group(2).strip('\n')
				#drop useless info in value
				value=re.sub(r'<a\s[^>]+?>([^<]*?)</a>',r'\1',value)#drop superlink
				value=re.sub(r'(?:&nbsp;)|(?:\"\+response\.[a-z]+\+\")|\s+',r'',value)
				tag=re.sub(r'\s+',r'',tag)
				#print(tag,value)
				#add to cache
				if (tag.find('生日')!=-1) and (value.find('座')!=-1):#.encode('UTF-8'):
					#drop data, continue
					continue
				else:
					self.data.addItem(tag,renrenId,value)
			except Exception as e:
				print(item)
