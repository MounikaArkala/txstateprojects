#
#   pso.fields.py  - Python Service Objects Form Tag lib
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
#   $Id: fields.py,v 1.5 2004/07/12 04:03:31 thanos Exp $
#
__version__="$Revision: 1.5 $"

from string import letters, digits
from form import  ValidationFailure,FieldMissing,  ValidationError, DefaultField, Select, Input
from isocodes import USStates
from validation import isZipCode

class StateSelect(Select):
	OPTIONS=( ('NN','Non US or Canada'), ) + USStates

	
			
			
			

	
class ZipInput(Input):
	def validate(self, handler):
		value = Input.validate(self, handler)
		if not value: return ''
		try:
			isZipCode(value)
		except Exception, e:	
			raise ValidationError(self.getName(), '%s' % e)
		return value


class PhoneInput(Input):
	def validate(self, handler):
		value = Input.validate(self, handler)
		if not value: return ''
		
		
	


class EmailInput(Input):
	def validate(self, handler):
		value = Input.validate(self, handler)
		if len(value):
			if value.count('@') != 1:
				raise ValidationError(self.getName(), 'invalid e-mail')
			if value.count('.') < 1:
				raise ValidationError(self.getName(), 'invalid e-mail')
		return value

class UrlInput(Input):
        def validate(self, handler):
                value = Input.validate(self, handler)
		if value:
			from urllib import urlopen
			try:
				urlopen(value)
			except:
				raise ValidationError(self.getName(), 'invalide url')
                return value

class UserIdInput(Input):
	SIZE=5

	VALIDCHAR = letters+digits
	REQUIRED=1

	def validate(self, handler):
		value = Input.validate(self, handler)
		v = [ch for ch in value if ch not in self.VALIDCHAR]
		if v:
			raise ValidationError(value, 'login id must be alphnumerical [a-z, A-Z, 0-9]')
		size = int(self.getAttrs().get('size', str(self.SIZE)))
		if len(value) < size:
			raise ValidationError(value, 'login id must be  %d character or longer' % size)
		return value




		
	


	
			
			
		
			 
		 
			
			
