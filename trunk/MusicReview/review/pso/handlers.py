#
#   handlers.py  - Python Service Objects
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
#   $Id: handlers.py,v 1.6 2003/11/18 19:04:22 thanos Exp $
#
__version__="$Revision: 1.6 $"

from service import OK
from parser import CachedParser


class TemplateHandler:
		
	TMPL="%s.html" 
	TMPL_PATH='templates/'
	def renderer(self, object, cdata=''):
		if object:
			return object.render(self, cdata)
		return cdata	

	def parse(self, req):
		self._req = req
		self._scratch={}
		
		try:
			template = self.buildTemplate(self.getTemplate(self.req()))
			tree = CachedParser().parseFile(template)
		except:
			import traceback
			traceback.print_exc()
			template = self.buildTemplate(self.getDefaultTemplate(req))
			tree = CachedParser().parseFile(template)
			
		html =  tree.render(self.renderer) 
		self._req = None
		return html

	def handle(self, req):
		print self.parse(req)
		return OK

	def req(self):
		return self._req

	def scratch(self):
		return self._scratch
	


	def buildTemplate(self, template):
		return self.TMPL_PATH+self.TMPL % template
		
	def getTemplate(self, req):
		return req.pso().getEnviron('PATH_INFO', self.getDefaultTemplate(req))

	def getDefaultTemplate(self, req):
		if not hasattr(self, 'DEFAULT_TEMPLATE'):
			raise 'please either define attribute DEFAULT_TEMPLATE or override %s' % self.getDefaultTemplate
		return self.DEFAULT_TEMPLATE
