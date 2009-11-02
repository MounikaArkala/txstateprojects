#
#   nsapy.py  - Python Service Objects
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
#   $Id: nsapyrequest.py,v 1.4 2002/06/19 15:32:44 thanos Exp $
#
__version__="$Revision: 1.4 $"





import os
from pso.request import ServiceRequest
from pso.requestimpl import RequestImpl

def buildEnviron( pblock, environ = {}):
	if pblock:
		buff = pblock.pblock2str()
		buff = buff.replace('\\"', 'MinggniM')

		list = buff.split( '"' )
		list = map(lambda var,oldsep='MinggniM',newsep='"':var.replace(oldsep, newsep), list)
		for n in range( 1, len( list ), 2 ):
			key = list[n-1][:-1]
			key = key.strip()
			environ[key]  = list[n]
	return environ


def envReKey(environ):
	keys = {
        "content-length": "CONTENT_LENGTH" ,
         "content-type": "CONTENT_TYPE"  ,
         "accept": "HTTP_ACCEPT"  ,
         "accept-encoding": "HTTP_ACCEPT_ENCODING"  ,
         "accept-language": "HTTP_ACCEPT_LANGUAGE"  ,
         "authorization": "HTTP_AUTHORIZATION"  ,
         "cookie" :"HTTP_COOKIE" ,
         "if-modified-since": "HTTP_IF_MODIFIED_SINCE"  ,
         "referer": "HTTP_REFERER"  ,
         "user-agent":"HTTP_USER_AGENT"  ,
         "auth-type": "AUTH_TYPE"  ,
         "path-info": "PATH_INFO"  ,
         "auth-user": "REMOTE_USER"  ,
         "keysize": "HTTPS_KEYSIZE"  ,
         "secret-keysize" :"HTTPS_SECRETSIZE" ,
         "ip": "REMOTE_ADDR"  ,
         "security_active": "HTTPS"  ,
         "host": "HTTP_HOST"  ,
         "server_hostname": "SERVER_NAME"  ,
	 "query" : "QUERY_STRING", 
         "clf-request" : "REQUEST_LINE", 
         "method" : "REQUEST_METHOD", 
         "uri" : "SCRIPT_NAME", 
         "protocol" : "SERVER_PROTOCOL"
    }
	newenv = {}
	for key, value in [(key, value) for key, value in environ.items() if key in keys]:
			newenv[key] = value
	return newenv	




class NsapyRequest(RequestImpl):
	""" Concrete Implementation class for a Nsapi Request """
	COOKIE_KEY='HTTP_COOKIE'
	def __init__(self, req=None):
		self._req= req

	def req(self):
		return self._req


	def getOutStream(self):
		return self.ostream

	def getCookieKey(self):
		return self.COOKIE_KEY

	def getEnviron(self, handler): 
		env = {}
		try:
				env.update( os.environ ) 
		except:
				pass 
		
		env = buildEnviron( self.req().pb, env )
		env = buildEnviron( self.req().sn.session_dns(), env )
		env = buildEnviron( self.req().sn.client(), env )
		env = buildEnviron( self.req().rq.reqpb, env )
		env = buildEnviron( self.req().rq.headers, env )
		env = buildEnviron( self.req().rq.srvhdrs, env )
		env = buildEnviron( self.req().rq.vars, env )
		env = envReKey(env)
		env["SERVER_PORT"] = env["SERVER_NAME"] = ''
		host = env["HTTP_HOST"]
		if ":" in host:
			host, port = host.split(":")
		env["SERVER_PORT"] = port
		env["SERVER_NAME"] = host
		if env.has_key('PATH_INFO'):
			env["SCRIPT_NAME"] = env["SCRIPT_NAME"][:-len( env["PATH-INFO"] )]
		env['SERVER_URL'] = "http://%(SERVER_NAME)s:%(SERVER_PORT)s" % env
		return env
	

	def send_http_header(self, handler):
		handler.write(str(self.getHeadersOut()))
		handler.write('\n')

	def getInputs(self, handler, key=None, default=None, index=0):
		from cgi import FieldStorage
		if handler.getEnviron('REQUEST_METHOD') in  ( "POST", "PUT" ):
			ln = int( self.req().rq.request_header( "content-length", self.sn ) )
			data = self.req().sn.form_data( ln )
			stdin = StringIO( data )
			form = FieldStorage(file = stdin, env = handler.getEnviron())
		else:
			form = FieldStorage(environ = handler.getEnviron())
		return form

	def getServerReturn(self):
		return SERVER_RETURN
		
		
	def syncHeadersOut(self, headers):
		for k,v in headers.flatten():
			self.req().rq.srvhdrs.nvinsert(k, v)
		


        
class NSAPYServiceRequest(ServiceRequest):
	def __init__(self, sessionImpl=None):
		ServiceRequest.__init__(self, NsapyRequest, sessionImpl)
