#
#   cgirequest.py  - Python Service Objects
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
#   $Id: cgirequest.py,v 1.8 2003/01/20 23:20:00 thanos Exp $
#
__version__="$Revision: 1.8 $"

import sys, operator, os
from request import  SERVER_RETURN
from requestimpl import RequestImpl
from copy import copy

	
class CgiRequest(RequestImpl):
	""" Concrete Implementation class for a CGI Request """

	COOKIE_KEY='HTTP_COOKIE'
	def __init__(self, req=None):
		#RequestImpl.__init__(self, req)
		self.ostream= sys.stdout

	def req(self):
		return self

	def getOutStream(self):
		return self.ostream

	def getCookieKey(self):
		return self.COOKIE_KEY

	def getEnviron(self, handler):
		env ={}
		keys = os.environ.keys()
		values = os.environ.values()
		map(operator.setitem, [env]*len(keys), keys, values)
		#import os
		#env = copy(os.environ)
		return env
		
	def send_http_header(self, handler):
		handler.write(str(handler.getHeadersOut()))
		handler.write('\n')

	def getInputs(self, handler):
		from cgi import FieldStorage
		return FieldStorage()

	def getServerReturn(self):
		return SERVER_RETURN

