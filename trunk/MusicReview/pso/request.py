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
#   $Id: request.py,v 1.19 2004/07/12 04:00:22 thanos Exp $
#
__version__="$Revision: 1.19 $"

from tempfile import mktemp
from types import StringType
import time
import sys

from session import Session, CookieFileImpl
from resultcodes import  HTTP_MOVED_PERMANENTLY, HTTP_MOVED_TEMPORARILY 
class SERVER_RETURN(Exception):pass
from urlparse import urlparse, urlunparse
try:
	from urllib import urlencode
except:
	pass
try:
	from url import Url
except:
	Url = None

	

class RequestIO:
	"""
	RequestIO is a proxy ouput  stream. Everything writen to it will be buffered until the headers are sent or complete. 
	Then the contents is flused to the real out stream.
	"""

	def read(self, n = -1): return ""
	def readline(self, length = None): return ""
	def readlines(self): return []
	def writelines(self, list):
		self.write(''.join(list))
	def isatty(self): return 0
	def seek(self, pos, mode = 0): pass

	def __init__(self):
		self.pos = 0
		self.headers_sent = 0
		self.out = ""
		self.header_out = None
        
	def write(self, s):
		if not s: return
		if not self.headers_sent:
			self.out += s
		else:
			self.getOutStream().write(s)
		self.pos += len(s)

	def flush(self): 
		self.getOutStream().write(self.out)
		self.out=""


	def getHeadersOut(self):
		if self.header_out is None:
			self.header_out = self.impl.getHeadersOut()
		return self.header_out

	def tell(self): return self.pos
	def close(self):   
		#if not self.headers_sent:	
		self.send_http_header()
		self.flush()

	def headersSent(self):
		self.headers_sent=1

	def __del__(self):
		self.close()

	def setHeaderOut(self, key, value): 
		""" 	set a header entry. If this 
			entry already exits overwrite it.
		"""
		if type(value) != StringType:
			value = str(value)
		self.getHeadersOut()[key] =  value

	def addHeaderOut(self, key, value): 
		""" 	add a header entry. 
		"""
		self.getHeadersOut().add(key, value)

	def removeHeaderOut(self, key): 
		del self.getHeadersOut()[key]


class ServiceRequest(RequestIO):
	""" Bridge class for a http service Request """
	inputs = None
	inputSeq = None
	inputDict = None
	cookies = None
	environ = None
	_session = None
	
	def __init__(self, implClass, req=None):
		RequestIO.__init__(self)
		self.impl = implClass()
		self.impl.setup(self, req)
		self.response=""
		self.status = self.getStatusCode(200)



	def __call__(self): 
		return self

	def pso(self):
		" returns proxy to pso object "
		return self

	def getOutStream(self):
		return self.impl.getOutStream()

	def getInStream(self):
		return self.impl.getInStream()

	def setup(self, serviceHandler, reqHandler): pass

	def close(self):
		RequestIO.close(self)
		if self._session is not None:
			self._session.save(self)
		
	#
	# basics
	#

	def getStatusCode(self, code):
		self.impl.getStatusCode(code)

	

	#
	#  environ
	#
	def getEnviron(self,  key=None, default = None): 
		"""	if key is not given returns a dict of 	
			the server environment.
			Otherwise returns the entry for key.
			If no entry is found returns None or default if given. 
		"""
		if self.environ is None:
			self.environ = self.impl.getEnviron(self)
		if key is None:
			return self.environ
		return self.environ.get(key, default)
	
	def setEnviron(self, key, value):
		self.getEnviron()[key] = value
	#
	#
	#



	#
	#
	# Session handling
	#	
	def getSession(self, sessionImplClass = CookieFileImpl, **parameters): 
		""" 	returns the current session. The session implentation
		    	class may be passed to sessionImplClass, which if None
			defaults to CookieFileImpl. The method can be passed keyword
			arguments which will be treated as HTTP directives
		"""
		if sessionImplClass:
			for k,v in parameters.items():
				self.setEnviron(k, v)
			self._session = Session(self, sessionImplClass())
			if self._session.isNew():
			    self.setSession(self._session)
		return self._session

        def setSession(self, session):
		self.impl.setSession(self, session)
	session = {} #property(getSession,setSession)

	

	#
	# Cookie handling
	#

	def getCookieKey(self):
		return self.impl.getCookieKey()
		
	def getCookies(self): 
		"""	req.getCookies()-> dict

			returns  a dictionary of cookies. 
		"""
		if self.cookies is None:
			cookies = self.getEnviron(self.impl.getCookieKey(), '')
			if cookies:
				from Cookie import SmartCookie
				self.cookies = SmartCookie()
				self.cookies.load(cookies)
			else:
				self.cookies = {}
		return self.cookies

		
	def getCookie(self, key, default=None): 
		"""	returns the cookie requested by 
			key otherwise returns default,
			if default is not given returns None.
		"""
		return self.getCookies().get(key, default)

	def setCookie(self, key, value, **attrs):
		"""	sets cookie, key, to value.
			Also will set any attributes given.
			e.g. request.setCookie("login",name, comment="user id") 
		"""
		cookiefmt = "%s=%s;"
		cookie = cookiefmt % (key, value)
		for k,v in attrs.items():
			cookie += cookiefmt % (k, v)
		self.addHeaderOut('set-cookie', cookie)

	def send_http_header(self, content_type='text/html'):
		"""	send to stdout the content headers. Each on a seperate line.
			contenttype has not been set it will default to 'text/html'. 
			Then send an extra newline
		"""
		#print
		if not self.getHeadersOut().has_key('content-type'):
			if not self.getHeadersOut().has_key('location'):
				if not self.getHeadersOut().has_key('status'):
					self.getHeadersOut()['content-type'] =  content_type
		self.impl.syncHeadersOut(self.getHeadersOut())
		self.headersSent()
		self.impl.send_http_header(self)
		self.flush()


	#
	# Control
	#

	def redirect(self, url, permanent=0):
		"""
			force an imediate redirect to given url.
		"""
		
		self.impl.redirect(self, url, permanent)

	def setStatus(self, status):
		"""
			set the HTTP return status. 
			This normally defaults to 200.
		"""
		self.setHeaderOut('status', status)

	def sendStatus(self, status):
		"""
			set the HTTP return status. 
			This normally defaults to 200.
		"""
		self.setStatus(status)
		self.impl.sendStatus(status)

	#
	# Input
	#
	def hasInput(self, key):
		"""req.hasInput(key) -> 1 | 0
		tests if a field in a form was filled.
		"""
		return self.getInputs().has_key(key)

	def hasInputs(self, *keys):
		return [key for key in keys if key in self.getInputs().keys()]
			
			

	def getInputs(self, key=None):
		"""req.getInput(key) -> FiledStorage| List of Fields
		if key is given will return a list of fields values for that key.
		if there are no values an empty list is returned.
		if no key is given returns the cgi.FieldStorage object.
		"""
		if not self.inputs:
			self.inputs = self.impl.getInputs(self)
		if not key:
			return self.inputs
		if hasattr(self.inputs, 'getlist'):
			return self.inputs.getlist(key)
		else:
			if self.inputs.has_key(key):	
				value =  self.inputs.getvalue(key)
				if value and type(value) is type([]):
					return value 
				else:
					return [value] 
			return []
			

	def getInputSeq(self):
		if not self.inputSeq:
			self.inputSeq=[]
			for key in self.getInputs().keys():
				values = self.getInputs(key)
				for value in values:
					self.inputSeq.append((key, value))
		return self.inputSeq
	def getInputDict(self):
		if not self.inputDict:
			self.inputDict={}
			for key in self.getInputs().keys():
				self.inputDict[key] = self.getInputs(key)
		return self.inputDict
			
	def getInput(self, key, default=None, index=None):
		"""req.getInput(key) -> String | default
			returns the given form field value as a String.
			If there are multiple values under the same key, 
			it will return the first in the list, unless index is given.
			If no value is found will return "", unless default is given.
		"""
		if not index:
			index =0
		try:
			return 	self.getInputs(key)[index]
		except:
		#	import traceback
		#	traceback.print_exc()
			return default
		
	def getFile(self, key, default=None):
		"""req.getFile(fieldname)-> Field
		returns an uploaded file. The filed has the usual cgi.Field members plus
		filename -  the given file name
		file -  the actual file uploaded
		tempname - is None until keep() is called.
		the methods:
		keep() - The file object is a temporay file 
			that will be deleted when the cgi terminates. keep asigns the file a 
			a temp file name.
		save(name) -  This method can be used to save the tempfile under the given name.
		"""
		if self.hasInput(key):
			file = self.getInputs()[key]
			if file.filename:
				file.__class__.tempname= None
				file.__class__.keep= keep
				file.__class__.save= save
				return file
		return default

	#
	# Utilities
	#
	_url = None
	def getUrl(self):
		if self._url is None:
			self._url= Url("http://%(HTTP_HOST)s%(REQUEST_URI)s" % self.getEnviron())
		return self._url

	#url = property(getUrl)

	def uriParts(self):
		if not Url:
			raise 'under mod_python urlparse has problems'
		url  = "http://%(HTTP_HOST)s%(REQUEST_URI)s" % self.getEnviron() 
		parts = list(urlparse(url))
		info_path = self.getEnviron('PATH_INFO','')
		path=parts[2]
		if info_path: 
			path,dummy = path.split(info_path)
		indx = path.rfind('/')
		if indx > -1:
			script = path[indx:]
			path = path[:indx]
		else:
			script = path
			path=''
		parts[2] = path
		parts.insert(3, script)
		parts.insert(4,  info_path)
		return parts


	def buildUri(self, parts, clean, **kws):
		query={}
		i = 0
		for key in ('scheme', 'netloc', 'path', 'script','pathinfo', 'param', 'fragment'):
			if kws.has_key(key):
				parts[i] = kws[key]
				del kws[key]
			i += 1

		if clean:
			 parts[6] =''
		qs = parts[6]
		if qs:
			if type((qs)) ==type(''):
			# now for QS key, values:
			#
				querySeq = parts[6].split('&')
				querySeq= map(lambda x: x.split('='), querySeq)
				for k,v in querySeq:
					if query.has_key(k):
						query[k].append(v)
					else:
						query[k] = [v]
		querySeq=[]
		query.update(kws)
		if query:
			for key,values in query.items():
				if type(values) == type([]):
					for value in values:
						querySeq.append((key, value))
				else:	
					querySeq.append((key, values))
			query = urlencode(querySeq, doseq=1)
		else:
			query = parts[6]
		if parts[4]:
			parts[2]= "%s%s%s"  %  tuple(parts[2:5])
		else:
			parts[2]= "%s%s"  %  tuple(parts[2:4])

		del parts[3:5]
		parts[4]= query
		return urlunparse(parts)
		
	def serviceUri(self, clean=1, **kws):
		parts = list(self.uriParts())
		url =  self.buildUri(parts, clean, **kws)
		return url

	def baseUri(self):
		parts = list(self.uriParts())
		return "%s://%s%s/" % tuple(parts[:3])
		
	def pageUri(self, page): 
		return self.baseUri() + page


	def log(self, *args):
		args = map(str, args)
		post = "\n%s: %s" % ( time.ctime(), ' '.join(args))
		try:
			sys.stderr.write(post)
		except:
			import traceback
			traceback.print_exc(file=self.stderr)
		
		
			

def keep(fileField): 
	""" req.getFile(key).keep() -> file 
		This method is added to file form fields.
		Files  that are uploaded are stored as nameless 
		temporary files. This method allows you to store the file,  so it can be 
		processed at a later stage. 
		Calling it replaces the nameless temp file with the new named temp file.
	"""
	if not fileField.tempname:
		fileField.tempname = mktemp()
		fileField.file.seek(0)
		fp = open(fileField.tempname,'wb')
		fp.write(fileField.file.read())
		fp.close()
		fileField.file= open(fileField.tempname)
		
	

def save(fileField, newName): 
	""" req.getFile(key).saveAs(somename) -> None
		This method is added to file form fields.
		Files  that are uploaded are stored as nameless 
		temporary files. This method alows you to store the file with a given name.
	"""
	if not fileField.tempname:
		fileField.keep()
		fileField.file.flush()
		fileField.file.close()
	import os
	os.rename(fileField.tempname, newName)
	

	
		

		




	

		



def psoTest(req):
	if not req:
		req = ServiceRequest()
	req.pso().send_http_header()
	try:
		session['reload'] +=1
	except:
		session['reload'] = 0
	req.pso().write("\n try reload ", req.pso().session)

def simpleTest():
	req = ServiceRequest()
	import sys
	sys.stdout = req
	print 1,"hello world"
	req.pso().send_http_header()
	req.pso().write(" 2. hello world")
	print 3, " third time"

def redtest1():
	import sys
	sys.stdout = req = ServiceRequest()
	print "hello",
	req.send_http_header()
	print "world"
	

def redtest2():
	req = ServiceRequest()
	print "hello",
	req.send_http_header()
	print "world"
            
if __name__ == '__main__':
	if 0:
		import pdb
		pdb.run("simpleTest()")
	else:
		redtest2()	
        
