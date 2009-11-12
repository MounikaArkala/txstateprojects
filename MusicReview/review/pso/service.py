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
#   $Id: service.py,v 1.10 2004/07/12 04:00:22 thanos Exp $
#
__version__="$Revision: 1.10 $"

import sys
from weakref import ref
from time import time, strftime, gmtime



from util import log
from request import ServiceRequest, SERVER_RETURN
from session import CookieFileImpl
from cgirequest import CgiRequest


		
		
		



        



OK = 0
def fixup(req, requestImpl, sessionImpl=CookieFileImpl): 
	sys.stdout = req.pso = ServiceRequest(requestImpl, req)
	session = req.pso().getSession( sessionImpl)

def cleanup(req):
	log('cleaing up', req)
	req.pso().close()


class ServiceHandler:
	PRODUCTION = 0
	def run(self, handler, sessionImpl =CookieFileImpl):
		try:
			stdout = sys.stdout
			stderr = sys.stderr
			sys.stdout = pso = ServiceRequest(CgiRequest)
			pso.stderr = stderr
			logfile = pso.getEnviron('PSOLog')
			if logfile:
				sys.stderr = open(logfile, 'a', 0)
			if sessionImpl:
				pso.session = pso.getSession( sessionImpl )
			status =  handler(pso)
		except SERVER_RETURN, status:
			pass
		except:
			sys.stdout = stdout
			import traceback
			if not self.PRODUCTION:
				traceback.print_exc(file = sys.stdout)
			else:
				traceback.print_exc()
			sys.stderr = stderr


def test(req):
	print "hello world"

def test1(req):
	print "hello world"
	req.send_http_header(content_type= 'text/plain')

def test2(req):
	print "hi there" 
	req.sendStatus(204)

def test3(req):
	print "hi there" 
	req.redirect("http://www.w3c.org/")

	
	

if __name__ =='__main__':
	ServiceHandler().run(test3)
	
		
        
