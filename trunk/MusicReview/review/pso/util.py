#
#   $RSCFile$  - Python Service Objects
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
#   $Id: util.py,v 1.11 2004/07/12 03:48:55 thanos Exp $
#
__version__="$Revision: 1.11 $"

import time, gc, sys, weakref
class Log:
	def __init__(self, path=None):
		self.logfile = path
	def log(self, *args):
		args = map(str, args)
		post = "\n%s: %s" % ( time.ctime(), ' '.join(args))
		try:
			open(self.logfile,'a').write(post)
		except:
			import traceback
			traceback.print_exc()
import os, tempfile
logger=Log(os.environ.get('PSOLOG',os.path.join(tempfile.gettempdir(), 'pso.log')))
log = logger.log
		

class MixIn:
	def getDirectives(self, objclass, reqHandler):
		directives ={}
		for key in objclass.DIRECTIVES: 
			lkey = objclass.DIRECTIVEtAG + key
			value = reqHandler.getEnviron( lkey)
			if value:
				directives[key] = value
		return directives

def mkDict(**kv):
	return kv

def get(dict,key, default=None):
	if dict.has_key(key):
		return dict[key]
	return default


"""
class GCDumper:
	def __init__(self):
		" set up gc in debug mode"
		gc.enable()
		gc.set_debug(gc.DEBUG_LEAK)
	def dump(self, file=None):
		" dumps to file, file=stdout by defaut, garbadgeed objects"
		gc.collect()
		if file is  None:
			file = sys.stdout
		for x in gc.garbage:
			strX = str(x)
			if len(strX) > 80: tail = '...'
			else: tail =''	
			file.write("%s: %s%s\n" % ( type(x), strX[:77], tail))

class meta_ObjTracker:
	classes = {}
	def instance(celf, obj):
		ref = weakref.ref(obj)
		key = obj.__class__.__name__
		try:
			celf.classes[key].append(ref)
		except:
			celf.classes[key] = [ref]
	instance = classmethod(instance)

	def report(celf, classes=None):
		if classes is None:
			classes = celf.classes.keys()
		else:
			classes = classes.split()
		classes.sort()
		for name in classes:
			for ref in celf.classes[name]:
				obj =ref()
				if obj is not None:
					print obj
	report = classmethod(report)
"""
	
	


			
		
if __name__ =='__main__':
	d = GCDumper()
	l =[]
	l.append(l)		
	del l
	d.dump()
	class A:
		def __init__(self):
			ObjTracker.instance(self)
	class B:
		def __init__(self):
			ObjTracker.instance(self)
	def test():
		a =A()
		b = B()
	for i in xrange(10): test()
	ObjTracker.report()

	
			
	






