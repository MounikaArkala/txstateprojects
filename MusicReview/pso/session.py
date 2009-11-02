#   session.py  - Python Service Objects
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
#   $Id: session.py,v 1.15 2004/07/12 03:52:06 thanos Exp $
#
__version__="$Revision: 1.15 $"

from weakref import ref
from time import time, strftime, gmtime
from  cPickle import load, dump
from tempfile import mktemp
from util import MixIn, log
import sys, os


try:
	mapClass = dict
except:
	import UserDict 
	mapClass = UserDict.UserDict


class SessionImpl:
	"abstract implementaion class"

	DEFAULTServiceIdKey = "PSOServiceId"
	DEFAULTSessionIdKey = "PSOSessionId"
	DEFAULTServiceIdValue = "SESSION_ID"


	def getServiceId(self,  reqHandler): 
		"""session.getServiceId(requestHandler) -> String ~ The service id, set in the HTTP directive, is returned. 
			This will default to the script's name"""
		return reqHandler.getEnviron(self.DEFAULTServiceIdKey, self.getDefaultServiceId())

	def getDefaultServiceId(self):
		return self.DEFAULTServiceIdValue

	def getSessionId(self,  reqHandler): 
		"""session.getSessionId(requestHandler) -> String | None ~ The current session id returned.   
			If none return None.
			By default will look for a HTTP directive <i>ServiceId</i>"""
		return reqHandler.getEnviron(self.DEFAULTSessonIdKey)
	def load(self,  reqHandler, session): 
		"session.load(requestHandler) -> Session"
	def save(self,  reqHandler, session): 
		"session.session(requestHandler, self) -> None"
	def revert(self,  reqHandler): 
		"session.revert(requestHandler, self) -> None ~reverts the session to last saved copy."
		
	def expire(self,  reqHandler, when): 
		"""
		session.expire(requestHandler, when) -> None ~ if when is evals 
		to a number  will expire the session in when seconds, otherwise will try and parse when as a date.
		For more on this format see <a href="http://www.faqs.org/rfcs/rfc2068.html">RFC2068</a> section 3.3.1 
		[also <a href="http://www.faqs.org/rfcs/rfc822.html">RCF822</a> and  
		<a href="http://www.faqs.org/rfcs/rfc1123.html">RCF1123</a>]
		"""
	def newSessionId(self): 
		""" session.newSessionId(self.requestHandler) -> String ~ returns a new sessionId, preferably unique."""
    
class Session(mapClass):
	"""Session Bridge"""
	def __init__(self, reqHandler, impl=None):
		"""session = Session(requestHandler, SessionImplmentor()) ~ ctor's a session with the given 
		request handler and session implementation instance"""
		mapClass.__init__(self)
		self.init(reqHandler, impl)
		self.setup()
        
	def init(self, reqHandler, impl):
		""" self.init(reqHandler, impl)-> None ~ template init method called by CTOR"""
		self.sessionId=None
		self.serviceId=None
		self.status='new'
		self.impl = impl
		#self.impl.session = ref(self)
		self.reqHandler= ref(reqHandler)
		#self.reqHandler= reqHandler
		self.expiresWhen=None
        
	def setup(self):
		""" self.setup()-> None ~ template method 
		used to define relationship between session and requestHandler"""
		self.serviceId= self.getServiceId()
		self.sessionId= self.getSessionId()
		if not self.isNew():
			self.load()

	def isNew(self):
		""" session.new()-> 1|0 ~ returns 1 if session was created on this request, otherwise 0 
		used to define relationship between session and requestHandler"""
		return self.status=="new"
		
	def getServiceId(self, reqHandler=None): 
		""" session.getServiceId()-> String ~ returns serviceId, request passed on to the implementor."""
		if reqHandler is None:
			reqHandler = self.reqHandler()
		if not self.serviceId:
			self.serviceId = self.impl.getServiceId(reqHandler)
		return self.serviceId

	def getSessionId(self, reqHandler=None): 
		""" session.getSessionId()-> String ~ returns either the current sessionId or a new session id."""
		if reqHandler is None:
			reqHandler = self.reqHandler()
		if not self.sessionId:
			self.sessionId = reqHandler.getEnviron(self.getServiceId(reqHandler))
			if not self.sessionId:
				self.sessionId = self.impl.getSessionId(reqHandler)
				if not self.sessionId:
					self.status = 'new'
					self.sessionId = self.impl.newSessionId(reqHandler)
					self.purge(reqHandler)
				else:
					self.status='open'
		return self.sessionId

	def purge(self, reqHandler=None): 
		self.impl.purge(reqHandler)


      
	def load(self, reqHandler=None): 
		""" session.load()-> None ~ loads a session into its self."""
		if reqHandler is None:
			reqHandler = self.reqHandler()
		try:
			session =  self.impl.load(reqHandler, self)
			if session:
				expires  = session.getExpire()
				if expires is not None and expires < time():
					self.status = "new"
					return 
				self.update(session)
			else:
				self.status = "new"

		except Exception, e:
			import traceback
			traceback.print_exc()
			self.status = "new"
		return {}

	def save(self, reqHandler=None): 
		""" session.save()-> None ~ saves self."""
		if reqHandler is None:
			reqHandler = self.reqHandler()
		self.reqHandler = None
		self.status = 'open'
		self.impl.save(reqHandler, self)
		self.reqHandler= reqHandler

	def getExpire(self):
		""" session.getExpire()-> float ~ returns when it will expire in secs since epoche."""
		return self.expiresWhen
		
	def expire(self, when = None): 
	#def expire(self, when = None): 
		""" session.expire(when)-> None ~ expires session at time.time() + when, 	
		if eval(when) evalutes, otherwise tries to parse when and expire session at when. 
		For more on this format see <a href="http://www.faqs.org/rfcs/rfc2068.html">RFC2068</a> section 3.3.1 
		[also <a href="http://www.faqs.org/rfcs/rfc822.html">RCF822</a> and  
		<a href="http://www.faqs.org/rfcs/rfc1123.html">RCF1123</a>]
		"""
		self.expireWhen = when
		self.impl.expire(self, self.reqHandler(), when)
		#self.impl.expire(self, self.req(), when)

	def setSession(self, reqHandler=None): 
		""" session.setSession() -> None ~ adds session to request handler. """ 
		if reqHandler is None:
			reqHandler = self.reqHandler()
		self.impl.setSession(self, reqHandler)
	
	




		
	

class FileLoader(MixIn):
	DIRECTIVEtAG='PSOSessionFileLoader_'	
	DIRECTIVES=('Path',)
	PATH = os.path.dirname(mktemp())
	def getFileName(self, reqHandler, session):
		"""session.getFileName(requestHandler) -> String ~ returns a fully qualified session file name."""
		path = self.getPath(reqHandler)
		file = session.getSessionId(reqHandler)
		filename =  os.path.join(path, file)
		return filename

	def getPath(self, reqHandler):
		""" session.getPath(requestHandler) -> String ~ returns the path where sessions will be stored."""
		return self.getDirectives(FileLoader, reqHandler).get('Path', self.PATH)
		
	def purge(self, reqHandler=None): pass
		

	def newSessionId(self, reqHandler):
		"""session.newSessionId(requestHandler) -> String ~ returns a new sessionId, preferably unique."""
		id =  os.path.basename(mktemp(self.getServiceId( reqHandler)))
		return id

	def load(self, reqHandler, session):
		"""session.load(requestHandler) -> session ~ returns session. All thrown expections passed on."""
		return load(open(self.getFileName(reqHandler, session),'r+b'))

	def save(self, reqHandler, session):
		""" session.save(requestHandler) -> None ~ saves session. All thrown expections passed on."""
		file = self.getFileName(reqHandler, session)
		f = open(file,'w+b')
		dump( session, f)

class CookieSession(MixIn):
	DIRECTIVEtAG='PSOCookieSession_'	
	DIRECTIVES=('expires', 'Path','Comment','Domain','Max-Age','secure','Version')

	def getCookie(self, reqHandler):
		""" self.getCookie(requestHandler) -> String | None ~ returns the session cookie if found
		otherwise none"""
		cookie = reqHandler.getEnviron(reqHandler.getCookieKey())
		if cookie:
			try:
				start=0
				look4 = self.getServiceId(reqHandler)+'='
				start = cookie.index(look4)
				start += len(look4)
				end = cookie.find(';', start)
				if end == -1:
					cookie = cookie[start:]
				else:
					cookie = cookie[start:end]
				return cookie.strip()
			except Exception, e:
				import traceback
				traceback.print_exc()
				return None

	def getSessionId(self, reqHandler): 
		"""self.getSessionId(requestHandler) -> String | None ~ The current session id returned.   
			If none return None."""
		return self.getCookie(reqHandler)


	def when(self, when):
		"""self.when(when) -> None ~ utility method to build the correct cookie expire attributes."""
		if not hasattr(self, 'attrs'):
			self.attrs = {}
		if when is not None:
			try:
				when = eval(str(when))
				when = time() + when 
				#self.attrs['Max-Age']= str(long(when))
				self.attrs['expires'] = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime(when))
			except:
				self.attrs['expires'] = when
				if self.attrs.has_key('Max-Age'):
					del self.attrs['Max-Age']
				

	
	def expire(self, session, reqHandler, when = None): 
		""" self.expire(session, requestHandler, when)-> None ~ expires session at time.time() + when, 	
	if eval(when) evalutes, otherwise tries to parse when and expire session at when. 
	For more on this format see <a href="http://www.faqs.org/rfcs/rfc2068.html">RFC2068</a> section 3.3.1 
	[also <a href="http://www.faqs.org/rfcs/rfc822.html">RCF822</a> and  
	<a href="http://www.faqs.org/rfcs/rfc1123.html">RCF1123</a>]
	"""
		self.when(when)
		reqHandler.setSession(session)

	def getAttrs(self):
		""" self.getAttrs() -> Dictionary of cookie attributes ~ utility 
			method for setting up the  session cookie"""
		if hasattr(self, 'attrs'):
			return self.attrs
		else:
			return {}

	def setSession(self, session, reqHandler):
		""" self.setSession(session, reqHandler) -> None ~ adds session to request handler.
			Handles setting the cookie when the session is new.
		""" 
		self.attrs = self.getAttrs()
		self.attrs.update(self.getDirectives(CookieSession, reqHandler))
		value = reqHandler.getEnviron('PSOSessionExpires')
		if value:
			self.when(value)
		reqHandler.setCookie(session.getServiceId(), session.getSessionId(), **self.getAttrs())


class CookieFileImpl(CookieSession, FileLoader, SessionImpl):
	""" Default session implementation, using temporary files to 
			store the session, and using a browser cookie to 
			pass the session id accross requests."""

class FileSession(Session ):
	""" Default session bridge, using CookieFileImpl as the implementaion class"""
        def init(self, reqHandler,imp):
            Session.init(self, reqHandler, CookieFileImpl())
            
			
		
        
