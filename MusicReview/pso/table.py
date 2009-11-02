#   table.py  - Python Service Objects
#
#   Author: Thanos Vassilakis thanos@@0x01.com
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
#   $Id: table.py,v 1.5 2002/06/19 15:23:25 thanos Exp $
#
__version__="$Revision: 1.5 $"
from types import ListType

try:
	mapClass = dict
except:
	import UserDict 
	mapClass = UserDict.UserDict

class Table(mapClass):
	def add(self, key, value):
		try:
			self[key.lower()].append(value)
		except:
			self[key.lower()] = [value]

	def set(self, key, value):
		self[key.lower()] = [value]

	def __repr__(self):
		text=""
		for k, v in self.flatten():
				text += "%s: %s\n" % ( k,v)
		return text

	def flatten(self):
		items=[]
		for key, values in self.items():
			if type(values) is ListType:
				for value in values:
					items.append((key,value))
			else:
				items.append((key,values))
		return items

class CIMap(mapClass):
	def __setitem__(self, key, item):
		mapClass.__setitem__(self, key.lower(), item)
	
		
				

if __name__ =='__main__':
	print Table.__bases__
	t = Table()
	t.add("cookie-set","me")
	t.add("cookie-set","you")
	t.add("max-set","1")
	t.set("max-set","2")
	print t
