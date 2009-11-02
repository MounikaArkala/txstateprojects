#
#   pso.url.py  - Python Service Objects
#
#   Author: Thanos Vassilakis thanos@0x01.com
#
#   	Copyright (c) thanos vassilakis 2000,2001, 2002
#
#	This library is free software; you can redistribute it and/or 
#	modify it under the terms of the GNU Lesser General Public License 
#	as published by the Free Software Foundation; either version 2.1 of the 
#	License, or (at your option) any later version.
#
#	This library is distributed in the hope that it will be useful, but 
#	WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
#	or FITNESS FOR A PARTICULAR PURPOSE.  
#	See the GNU Lesser General Public License for more details.
#
#	See terms of license at gnu.org. 
#
#   $Id: url.py,v 1.5 2004/07/12 03:50:05 thanos Exp $
#
# created: thanos vassilakis 1/21/2001
#
# LGPL
#
#
__version__="$Revision: 1.5 $"

from urlparse import urlsplit, urlunsplit
from cgi import parse_qs
from urllib import urlencode
from xml.sax.saxutils import quoteattr
from copy import deepcopy

class Url(object):
	_query=None
	_script=None
	def __init__(self, url, scheme="html"):
		self.scheme, self.netlocation, self.path, query, self.fragment = urlsplit(url, scheme)
		self.queryTD = self.decryptQuery(query)
		self.changed=1
		self._formFields =""

	def decryptQuery(self, query): return query

	def encryptQuery(self, query): return query
		
	def processQuery(self):
		if self._query is None:
			self._query = parse_qs(self.queryTD)
		return self._query
	query = property(processQuery)

	def getScript(self):
		if self.changed or self._script is None:
			self._script = urlunsplit((self.scheme, self.netlocation, self.path,'',''))
		return self._script
	script = property(getScript)


	def getBase(self):
		if self.changed or self._script is None:
			self._script = urlunsplit((self.scheme, self.netlocation, '','',''))
		return self._script
	base = property(getBase)
		

	def __setitem__(self, key, value):
		self.changed=1
		self.query[key] = value
	def __delitem__(self, key):
		try:
			self.changed=1
			del self.query[key]
		except:
			pass
	def __getitem__(self,key):
		value=  self.query.get(key, None)
		if type(value) is type([]):
			if len(value) == 1:
				return value[0]
		return value

	def clear(self, *args):
		if not args:
			self.query.clear()
		else:
			for arg in args:
				del self[arg]


	def append(self, key, value):
		self.changed=1
		try:
			self.query[key].append(value)
		except:
			self.query[key]=[value]
	
	NDICT={}
	def __str__(self):
		if self.changed:
			self.queryTD= urlencode(self.query, self.query.items())
		return urlunsplit((self.scheme, self.netlocation, self.path, self.encryptQuery(self.queryTD), self.fragment))

	def getFormFields(self):
		if self.changed:
			self._formFields =""
			for k, values in self.query.items():
				if values:
					if type(values) is type([]):
						for v in values:
							self._formFields = '%s\n<input type="hidden" name="%s" value="%s" >' % (self._formFields, k, v)
					else:
						self._formFields = '%s\n<input type="hidden" name="%s" value="%s" >' % (self._formFields, k, values)
		return self._formFields
	formFields = property(getFormFields)



	def copy(self):
		return deepcopy(self)

	def uri(self, **kws):
		query ={}
		if not kws.get('_cleanup', True):
			query.update(self.query)
		for k,v in kws.items():
			if v is None:
				del kws[k]
				if k in query:
					del query[k]
			else:
				query[k] = v
		query = self.encryptQuery(urlencode(query, query.items()))
		return urlunsplit(('','',self.path, query, ''))

	def aHref(self, cdata, **kws):
		query = self.encryptQuery(urlencode(kws, kws.items()))
		return '<a href="%s">%s</a>' %(urlunsplit(('','',self.path, query, '')), cdata)

	def newA(self, uri, cdata, **attr):
		attrlist = ["%s=%s" % (k, quoteattr(v)) for k,v in attr.items() if v]
		attrlist.extend([k for k,v in attr.items() if not v])
		attrlist = ' '.join(attrlist)
		return '<a href="%s" %s>%s</a>' %( uri, attrlist, cdata)
				



		

