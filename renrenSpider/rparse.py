_nameprog=None
def friendList(pfHrefs):
	"""friendList('{<a href="...?id=1">name1</a>,<a href="...?id=3">name2</a>}') 
	--> {id1:name1,id2:name2}"""
	global _nameprog
	if _nameprog is None:
		import re
		_nameprog=re.compile(r'id=(\d+)">([^<]*?)</a>')

	if isinstance(pfHrefs,str):
		pfHrefs={pfHrefs}
	name=dict()
	for pfHref in pfHrefs:
		m=_nameprog.search(pfHref)
		if m is None: return None
		name[m.group(1)]=m.group(2)
	return name
