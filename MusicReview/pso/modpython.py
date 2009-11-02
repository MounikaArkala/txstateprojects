#
#   modpython.py  - Python Service Objects
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
#   $Id: modpython.py,v 1.10 2002/06/19 15:34:51 thanos Exp $
#
__version__="$Revision: 1.10 $"

from operator import setitem, getitem

from pso import service
from cgirequest import CgiRequest

from mod_python import apache, util

def fixup(req, sessionImpl=None): 
	service.fixup(req, ModPythonRequest, sessionImpl = sessionImpl )
	return apache.OK

def cleanup(req):
	service.cleanup(req)
	return apache.OK


class FormInput(util.FieldStorage):
	def getvalue(key, default=None):
		reval = default
		if self.has_key(key):
			value = self[key]
			if type(value) is type([]):
				retval =  map(lambda v:v.value, value)
			else:
				retval =  value.value
		return retval
	
	def getfirst(self, key, default =None):
		retval = default
		if self.has_key(key):
			value = self[key]
			if type(value) is type([]):
				retval =  value[0].value
			else:
				retval =  value.value
		return retval
	
	
	def getlist(self, key):
		if self.has_key(key):
			value = self[key]
			if type(value) is type([]):
				return value
			else:
				return [value]
		return []
	
		
			

class ModPythonRequest(CgiRequest):
	""" Concrete Implementation class for a mod_python Request """
	#COOKIE_KEY='Cookie'

	def req(self):
		return self._req
		
	def setup(self, handler, req): 
		#req.pso = handler
		self._req = req



	def getOutStream(self):
		return self.req()

		
	def getEnviron(self, handler): 
		self.req().add_common_vars()
		env = {}
		subenv = self.req().subprocess_env
		keys = subenv.keys()
		values = map(getitem, (subenv,)*len(keys), keys)
		map(setitem, [env]*len(keys), keys, values)
		env["GATEWAY_INTERFACE"] = "Python-CGI/1.1"
		if len(self.req().path_info) > 0:
			env["SCRIPT_NAME"] = self.req().uri[:-len(self.req().path_info)]
		else:
			env["SCRIPT_NAME"] = self.req().uri
		if self.req().headers_in.has_key("authorization"):
			env["HTTP_AUTHORIZATION"] = self.req().headers_in["authorization"]
		options = self.req().get_options()
		keys = options.keys()
		values = map(getitem, (options,)*len(keys), keys)
		map(setitem, [env]*len(keys), keys, values)
		return env

	def send_http_header(self, handler, content_type='text/html'): 
		self.req().content_type =  content_type
		self.req().send_http_header() 

	def getInputs(self, handler, key=None, default=None, index=0):
		from modpython import FormInput
		return FormInput(self.req())

	def getServerReturn(self):
		return apache.SERVER_RETURN

	def getHeadersOut(self):
		return self.req().headers_out
		
	def syncHeadersOut(self, headers): pass
		#self.req().headers_out.add('cookie','MyMi')
		#for k,v in headers.flatten():
		#	self.req().headers_out.add(k,v)
		
