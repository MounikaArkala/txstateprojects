#
#   requestimpl.py  - Python Service Objects
#
#   Author: Thanos Vassilakis thanos@0x01.com
#
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
#   $Id: requestimpl.py,v 1.5 2002/06/19 15:32:44 thanos Exp $
#
__version__="$Revision: 1.5 $"

from resultcodes import  HTTP_MOVED_PERMANENTLY, HTTP_MOVED_TEMPORARILY 
from table import Table



class RequestImpl:
	_req=None
	def getOutStream(self): pass
	def getInStream(self): pass
	def getStatusCode(self, code): pass
	def getEnviron(self):pass 
	def getCookieKey(self): pass
	def send_http_header(self): pass

	def setup(self, handler, req):  pass
	def req(self):
		return self._req
	

        def setSession(self, handler, session): 
		session.setSession()
		
	def addHeaderOut(self, handler, key, value): 
		self.getHeadersOut().add(key, value)



	def redirect(self, handler, url, permanent):
		handler.setHeaderOut('location', url)
		if permanent:
			status = HTTP_MOVED_PERMANENTLY
		else:
			status = HTTP_MOVED_TEMPORARILY
		raise self.getServerReturn(), self.getStatusCode(status)

	
	def getStatusCode(self, code):
		return code

	def getServerReturn(self,code): 
		return SERVER_RETURN


	def getHeadersOut(self):
		return Table() 
	def syncHeadersOut(self, headers): pass

	def sendStatus(self, status):
		raise self.getServerReturn(), self.getStatusCode(status)

	def getInputs(self): pass
