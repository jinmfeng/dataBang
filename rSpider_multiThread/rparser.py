import re

class rParser:
	#return a dict.
# key   -- renrenId of a friend, 
# value -- name of it.
	def friendList(self,items):
		name=dict()
		ptn=re.compile(r'id=(\d+)">([^<]*?)</a>')
		for item in items:
			m=ptn.search(item)
			if m == None:#parse error, return
				return -1 
			name[m.group(1)]=m.group(2)
		return name
