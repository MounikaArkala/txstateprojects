#
#   pso.form.py  - Python Service Objects Form Tag lib
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
#   $Id: form.py,v 1.8 2004/07/12 04:03:07 thanos Exp $
#
__version__="$Revision: 1.8 $"

from types import ListType, TupleType, StringType
import md5


from parser import Tag
from util import mkDict, log




class FormException(Exception):pass
class FieldMissing(FormException):
		def __init__(self, field, message='is mandatory'):
			self.field=field
			self.message=message
			Exception.__init__(self, message)

class ValidationError(FormException):
		def __init__(self, field, message):
			self.field=field
			self.message=message
			Exception.__init__(self, message)

class ValidationFailure(FormException):
		def __init__(self, errors):
			self.errors=errors
			Exception.__init__(self, message)




		

	

class FormPart(Tag):

	# states
	FORMsTATEkEY="formState"
	START = "start"
	INeRROR = "error"
	INcONFIRM="confirm"
	INsUBMIT = "submit"

	def getState(self, handler):
		state  = handler.scratch().get(self.FORMsTATEkEY, FormPart.START)
		return state


class Form(FormPart):
	def init(self):
		Tag.init(self)

	def validator(self, obj, cdata):
		if obj is not self:
			if obj and hasattr(obj, 'validate'):
				try:
					self.handler.scratch()[obj] = obj.validate(self.handler)
				except (ValidationError, FieldMissing), e:
					self.handler.scratch()[obj] = e
					self.handler.scratch()['errors'] = e
				except Exception, e:
					print child,  e
			


	def validate(self, handler):
		handler.scratch()['errors'] = []
		self.handler= handler
		self.travers(self.validator)
		self.handler= None


	def preProcess(self, handler):
		if handler is self: return ''
		prevState = handler.req().getInput(self.FORMsTATEkEY)
		if not prevState: # first time
			currentState =  Form.START
		elif prevState in  (Form.START, Form.INeRROR):
			if handler is not self:
				self.validate(handler)
				if handler.scratch()['errors']:
					currentState = Form.INeRROR
				else:
					currentState = Form.INcONFIRM
		elif prevState == Form.INcONFIRM:
			currentState = Form.INsUBMIT
		else:
			currentState =  Form.START
		handler.scratch()[self.FORMsTATEkEY] = currentState
		return ''
		




	def __call__(self, handler, cdata=''):
		table =  {
		Form.START: self.renderForm,
		Form.INeRROR: self.renderForm,
		Form.INcONFIRM: self.renderConfirm,
		Form.INsUBMIT: self.doSubmit
		} 
		method = table[self.getState(handler)]
		return method(handler, cdata)

	
	def renderHidden(self, hidden):
		if hidden:
			html=''
			for k,v in hidden.items():
				html += '<input type="hidden" name="%s" value="%s">' % (k,v)
			return html

	def getHidden(self, handler):
		return {}


	def getAction(self, handler): 
		action = self.attrs.get('action')
		if not action:
			url = handler.req().getUrl()
			url.clear()
			action = str(url)
		return action
	

	def renderForm(self, handler, fields):
		action = self.getAction(handler)
		if action:
			formattrs = self.buildAttrs( action = action)
		else:
			formattrs = self.buildAttrs()
		hidden =  self.getHidden(handler)
		hidden['action']= handler.req().getInput('action')
		hidden[self.FORMsTATEkEY] = self.getState(handler)
		hidden = self.renderHidden(hidden)
		return "<form %s>\n %s %s</form>" % ( formattrs, hidden,  fields)

	def renderConfirm(self, handler, cdata=''):
		return self.renderForm(handler, cdata)

	def onSubmit(self, handler):
		return handler.req().hasInputs('submit.x', 'submit') 

	def onConfirmed(self, handler):
		return handler.req().hasInputs('confirm.x','confirm') 

	def goNext(self, handler, cdata):
		handler.req().log( "GOTO NEXT PAGE")
		return "GOTO NEXT PAGE"

	def submit(self, handler, cdata):
		handler.req().log(handler.req().getInputs())

	def doSubmit(self, handler, cdata):
		self.submit(handler, cdata)
		self.goNext(handler, cdata)
		return "form submitted"
		
		
			
class Field(FormPart):
	REQUIRED=0

	def getName(self):
		return self.getAttrs()['name']	

	def getStartValue(self, handler, name):
		startvalue = self.getAttrs().get('value','')
		if hasattr(self, 'record'):
			record = self.fromDb(self.record(handler))
			#if name=='spam':
			if record:
				startvalue = record.get(name, startvalue) 
		value =	self.getFormValue(handler, name)
		if not value:
			 return startvalue
		return value

	def getFormValue(self, handler, name, default = ''):
		return handler.req().getInput(name,  default)

	def fromDb(self, value):
		return value
		
		
	def getValue(self, handler):
		name = self.getName()
		if self.getState(handler) is Form.START:
			value =   self.getStartValue(handler, name)
		else:
			value =  self.getFormValue(handler, name)
		return value


	def isGiven(self, handler):
		name = self.getName()
		value =	self.getFormValue(handler, name)
		if (self.REQUIRED or self.getAttrs().get('required')) and not value:
			raise FieldMissing(self.getName())
		return value
	
		
	def validate(self, handler):
		return self.isGiven(handler)

	def cData(self, handler, cdata):
		return cdata
		
	def __call__(self, handler, cdata=''):
		if self.getAttrs().get('readonly'):
			value = self.getValue(handler)
			return self.renderReadOnly(handler, value, self.cData(handler, cdata))
		if self.getState(handler) is Form.START:
			value = self.getValue(handler)
			return self.renderEditable(handler, value, self.cData(handler, cdata))

		if self.getState(handler) is Form.INeRROR:
			value =  handler.scratch().get(self, '')
			if isinstance(value, FormException):
				return self.renderInError(handler, value, self.cData(handler, cdata))
			else:
				return self.renderEditable(handler, value, self.cData(handler, cdata))

		if  self.getState(handler) is Form.INcONFIRM:
			value =  handler.scratch().get(self, '')
			#value = self.getValue(handler)
			return self.renderReadOnly(handler, value, self.cData(handler, cdata))


		value = self.getValue(handler)
		return self.renderEditable(handler, value, self.cData(handler, cdata))


	def buildAttrs(self, handler, **kws):
		return Tag.buildAttrs(self, **kws)

	def renderInError(self, handler, value, cdata):
		return '<font color="red">%s <- %s: %s </font>'  % (self.renderEditable(handler, self.getValue(handler), cdata), self.getName(), value)


	def renderEditable(self, handler, value, cdata):
		if cdata:
			return "<%s %s>%s</%s>" % (self.getAttrs()['tagname'], self.buildAttrs(handler, value=value) ,cdata, self.getAttrs()['tagname'])
		else:
			return "<%s %s />" % (self.getAttrs()['tagname'], self.buildAttrs(handler, value=value) )

	def renderReadOnly(self, handler, value, cdata):
		return """<i>%s</i><input type="hidden" name="%s" value="%s">""" % (value, self.getName(), self.getValue(handler))

	def renderReadOnly(self, handler, values, cdata):
		html=  """%s<input type="hidden"  name="%s" value="%s">""" 
		name = self.getName()
		if type(values) is type([]):
			fields = map(lambda n,v,h=html: h % (v,n,v), ( name,)*len(values), values)
			return ','.join(fields)
		return """<i>%s</i><input type="hidden" name="%s" value="%s">""" % (values, self.getName(), self.getValue(handler))


class DefaultField(Field):
	TYPE=None
	NAME=None
	EXT=""
	def init(self):
		Field.init(self)
		if self.TYPE:
			self.getAttrs().setdefault('type',self.TYPE)
		if not self.getAttrs().has_key('name'):
			if not self.NAME:
				name = self.__class__.__name__[:-len(self.EXT)]
				self.NAME = name[0].lower()+name[1:]
			self.getAttrs()['name'] = self.NAME



class Input(DefaultField):
	EXT="Input"

class Group(DefaultField):
	EXT="Group"
	def renderEditable(self, handler, value, cdata):
		return cdata

class ReadOnly(DefaultField):
	EXT="ReadOnly"
	def init(self):
		self.getAttrs()['readonly']=1
		DefaultField.init(self)

	
class Hidden(ReadOnly):
	TYPE="hidden"
	EXT="Hidden"
	def renderReadOnly(self, handler, value, cdata):
		return """<input type="hidden"  name="%s" value="%s">""" % (self.getName(), self.getValue(handler))




class Multiple(DefaultField):
	CHECKED="checked"
	VALUE = "value"

	def getFormValue(self, handler, name, default = ''):
		return handler.req().getInputs(name)

	def buildAttrs(self, handler, **kws):
		attrs = self.processAttrs( **kws)
		givenValues = self.getValue(handler)
		if type(givenValues) != type([]):
			givenValues = [givenValues]
		value = self.getAttrs().get('value')
		if value:
			if value in givenValues:
				attrs[self.CHECKED]=None
			elif attrs.has_key('checked'):
				del attrs[self.CHECKED]
		return DefaultField.buildAttrList(self, attrs)

		
	
	

class CheckBox(Multiple):
	EXT="CheckBox"
	TYPE="checkbox"

	def renderEditable(self, handler, value, cdata):
		value = self.getAttrs().get('value','')
		#return value, self.buildAttrs(handler, value=value)
		return DefaultField.renderEditable(self, handler, value, cdata)



class Radio(CheckBox):
	TYPE="radio"
	EXT="Radio"
	

class Options(Field):
	def getFormValue(self, handler, name, default = ''):
		name = self.getName()
		return handler.req().getInputs(name)

	def renderEditable(self, handler, value, cdata):
		return cdata #self.renderReadOnly(handler, values, cdata)

	def renderReadOnly(self, handler, values, cdata):
		html=  """%s<input type="hidden"  name="%s" value="%s">""" 
		name = self.getName()
		if type(values) is type([]):
			fields = map(lambda n,v,h=html: h % (v,n,v), ( name,)*len(values), values)
			return ','.join(fields)
		return values



class Submit(DefaultField):
	EXT="Submit"
	TYPE="submit"
	def buildAttrs(self, handler, **kws):
		if self.getState(handler)== Form.INcONFIRM:
			kws['name']="confirm"
		else:
			kws['name']="submit"
		return DefaultField.buildAttrs(self, handler, **kws)
	
	def renderReadOnly(self, handler, value, cdata):
		return self.renderEditable(handler, value , cdata)

class Select(DefaultField):
	EXT="Select"
	OPTIONS=[]
	FIRSTSplit="|"
	SECONDSplit=","


	def init(self):
		DefaultField.init(self)
		self.OPTIONS= self.getOptions()


	def renderEditable(self, handler, value, cdata):
		options = self.getOptionList(value)
		if options:
			cdata = options
		return DefaultField.renderEditable(self, handler, value, cdata)


	def getLabel(self, value):
		#MING 03-15-2004 some options are list of strings and some are list of tuples. Also, sometimes the first option might be empty string. Therefore can't always index o with 0
		for o in self.OPTIONS:
			if type(o) == StringType:
				if o == str(value):
					return o
			elif str(o[0]) == str(value):
				return o[1]
		
	def renderReadOnly(self, handler, value, cdata):
		return """<i>%s</i><input type="hidden" name="%s" value="%s">""" % (self.getLabel(value), self.getName(), self.getValue(handler))

	def getOptionList(self, selected):
		options = self.OPTIONS
		optionList=""
		for o in options:
			if type(o) in (ListType, TupleType):
				olen = len(o)
				if  olen ==3:
					value, label, chosen = o
				else:
					value, label, chosen = o[0],o[1],''
			else:
				value, label, chosen = o, o, ''
			if str(value) == str(selected):
				chosen='selected'
			optionList = '%s<option value="%s" %s>%s</option>' % ( optionList, value, chosen, label)
		return optionList

	def getOptions(self):
		options =  self.getAttrs().get('options')
		if options is None:
			return self.OPTIONS
		options = options.split(self.FIRSTSplit)
		options =  map(lambda x, ch=self.SECONDSplit : x.split(ch), options)
		if len(options[0]) == 1:
			options = map(None, options, options)
		return options


class TextArea(DefaultField):
	EXT="TextArea"
	
	def cData(self, handler, cdata):
		value = self.getValue(handler) 
		if value:
			cdata = value
		return  DefaultField.cData(self, handler, cdata)
	
class File(DefaultField):
	EXT="File"
	TYPE="file"
	CURRENTLABEL="<br><i>current choice: %s </i>"
	SAVEDAS= "savedAs"
	SAVED= "saved"
	READoNLYhTML ="""<i>%(filename)s</i><input type="hidden" name="%(saved)s" value="%(filename)s"><input type="hidden" name="%(savedAs)s" value="%(tempname)s">""" 

	def getStartValue(self, handler, name):
		filename =  DefaultField.getStartValue(self, handler, name+self.SAVED)
		tempname =  DefaultField.getStartValue(self, handler, name+self.SAVEDAS)
		return filename, tempname
		 
	def getFormValue(self, handler, name, default = ''):
		file =  handler.req().getFile(name)
		if file is None or type(file) is type(""):
			return default #self.getStartValue(handler, name)
		else:
			file.keep()
			return file.filename, file.tempname

	
		
	def renderEditable(self, handler, file, cdata):
		filename =''
		current =''
		if not (file is None or type(file) is type("")):
			filename, tempname  = file
			#if filename and tempname:
			current = self.getAttrs().get('currentlabel',self.CURRENTLABEL) %  self.readOnly(tempname,  filename)
		return DefaultField.renderEditable(self, handler, filename, cdata) +  current


	def renderReadOnly(self, handler, file, cdata):
		if not (file is None or type(file) is type("")):
			filename, tempname  = file
		else:
			filename =''
			tempname = ''
		return self.readOnly(filename, tempname)

	def readOnly(self, filename,  tempname):
		name = self.getName()
		attrs = mkDict(saved= name+self.SAVED, savedAs = name+self.SAVEDAS, filename=filename, tempname= tempname)
		return  self.READoNLYhTML % attrs
		

class PasswordEncoder:
	def encode(self, x):
		if x[:2] !='x:':
			return	'x:' + self.crypt(x)
		return x
		
	def crypt(self, x):
		egg = md5.new(x)
		return egg.hexdigest()
	
class PasswordGroup(PasswordEncoder, Group): 
	def renderReadOnly(self, handler, value, cdata):
		value = self.encode(value)
		return """<input type="hidden" name="%s" value="%s">""" % (self.getName(), value)

	
class PasswordInput(PasswordEncoder, Input): 
	TYPE="password"
	SIZE=7
	REQUIRED=1
	def renderReadOnly(self, handler, value, cdata): 
		return """<input type="hidden" name="%s" value="%s">****""" % (self.getName(), value)
		

	def validate(self, handler):
		value = Input.validate(self, handler)
		size = int(self.getAttrs().get('size', str(self.SIZE)))
		if len(value) < size:
			raise ValidationError(self.getName(), 'must be  %d characters or longer' % size)
		return self.encode(value)


class PasswordConfirmInput(PasswordInput): 
	def validate(self, handler):
		value = self.encode(Input.validate(self, handler))
		passwd =  self.encode(handler.req().getInput('password'))
		if passwd != value:
			raise ValidationError(self.getName(), 'must be the same as what you entered for <i>password</i>')
		return value
	
		
	
		
	
			

			
