#
#   tags.py  - Python Service Objects
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
#   $Id: tags.py,v 1.9 2003/11/18 19:04:23 thanos Exp $
#
from parser import Tag
from handlers import TemplateHandler
import sys
from cStringIO import StringIO

from util import log


class Template(Tag, TemplateHandler):
	FIELD_NAME='action'

	def getTemplate(self, req):
		return req.getInput(self.FIELD_NAME, self.getDefaultTemplate(req))
		
	def __call__(self, handler, cdata=''):
#		return self.getTemplate( handler)
		return self.parse(handler.req())

	def getDefaultTemplate(self, req):
		default = self.attrs.get('default')
		if not default:
			raise 'please set tag attribute default or override me %s' % self.getDefaultTemplate
		return default


class Exec(Tag):
	def __call__(self, handler, cdata=''):
		if not cdata:
			return ''
		oldout = sys.stdout
		try:
			sys.stdout = StringIO()
			exec cdata
			retval = sys.stdout.getvalue()
			sys.stdout.close()
		finally:
			sys.sdtout = oldout
		return retval	
		
class DataMixin:		
	KEY=None
	
	def getKey(self, handler): 
		return self.KEY
	def getRecId(self, handler, key): 
		return handler.req().getInput(key)

	def getRecord(self, handler, key): pass

	def record(self, handler): 
		key = self.getRecId(handler, self.getKey(handler))
		if key:
			scratchKey = (self.DATAMODEL, key)
			record = handler.scratch().get(scratchKey)
			if not record:
				record = self.getRecord(handler, key)
				if record:
					handler.scratch()[scratchKey] = record
			return record
			
		
	def getSelect(self, handler): pass
		
	def getSelection(self, handler, select): pass
	def getRecNumber(self, handler): 
		return len(self.selection(handler))

	
		
	def selection(self, handler): 
		criteria = self.getSelect(handler)
		scratchKey = (self.DATAMODEL, 'select', tuple(criteria.items()))
		cursor = handler.scratch().get(scratchKey)
		if not cursor:
			cursor = self.getSelection(handler, criteria)
			if cursor:
				handler.scratch()[scratchKey] = cursor
		return cursor

class OutLine(Tag):
	DELIMITER=','
	LI='<li>%s</li>'
	NAME=''

	def getValue(self, handler):
		field = self.attrs.get('name', self.NAME)
		value = self.record(handler).get(field)
		return value

	def getList(self, value):
		value = value.strip()
		delimiter = self.attrs.get('delimiter', self.DELIMITER)
		list = value.split(delimiter)
		return list
		
	def __call__(self, handler, cdata=''):
		try:
			return ''.join(map(lambda x: self.LI % x, self.getList(self.getValue(handler))))
		except:
			return ''
		
class Condition(Tag):
	def toShow(self, handler):
		return 1
	
	def __call__(self, handler, cdata=''):
		if self.toShow(handler):
			return cdata
		return ''
		
	
class Label(Tag):
	def toShow(self, handler):
		field = self.attrs.get('field')
		return field and self.record(handler).get(field)
		
		
		
				
class List(Tag):
	PAGEsIZEkEY="pagesize"
	LINEkEY="line"
	PAGEsIZE= 10
	HTML = '<a href="%s">%s</a>'
	NA='NA'
	ROWfIELDS=()

	def fetch(self, handler, line, pageSize): 
		cursor = self.selection(handler)
		return cursor.fetch(line=line, pageSize= pageSize)
		
	
	def __call__(self, handler, cdata):
		records = self.getRows(handler)
		html = ''
		for record   in records:
			html += cdata % self.prepareRow(handler, record)
		return html

	def getPageSize(self, handler):	
		return  int(handler.req().getInput( self.PAGEsIZEkEY, self.getAttrs().get(self.PAGEsIZEkEY, self.PAGEsIZE)))

	def getLine(self, handler):	
		return  int(handler.req().getInput( self.LINEkEY, self.getAttrs().get(self.LINEkEY, '1')))

	def getRows(self, handler): 
		return self.fetch(handler, line=self.getLine(handler), pageSize= self.getPageSize(handler))
		
	def prepareRow(self, handler, record):
		for field in self.ROWfIELDS:
			if field  not in record:
				record[field] = self.NA 	
		" must return an dictionary  of  fields that will be merged with the cdata"
		return record

	def next(self,  handler, cdata):
		line = self.getLine(handler)
		pageSize = self.getPageSize(handler)
		if line <  self.getRecNumber(handler) - pageSize:
			url = handler.req().getUrl().copy()
			url[self.LINEkEY] = line + pageSize
			return self.HTML % (url, self.getEnabled(cdata)) 
		else:
			return self.getDisabled(cdata)

	def prev(self,  handler, cdata):
		line = self.getLine(handler)
		pageSize = self.getPageSize(handler)
		if line >  pageSize:
			url = handler.req().getUrl().copy()
			url[self.LINEkEY] = line - pageSize
			return self.HTML % (url, self.getEnabled(cdata)) 
		else:
			return self.getDisabled(cdata)


		
	def getEnabled(self, cdata):
		return cdata
	def getDisabled(self, cdata):
		return cdata

			
	
class TwoColumnList(List):
	ACTION=''
	def getRows(self, handler): 
		rows = List.getRows(self, handler)
		if len(rows) % 2:
			if type(rows) is type([]):
				rows = tuple(rows)
			rows = rows + ('',)
		return [ i for n,i in zip(xrange(100),  zip(rows, rows[1:])) if n % 2==0]
			
	def prepareRow(self, handler, record):
		url = handler.req().getUrl().copy()
		row={}
		row['uri0'] =  url.uri(action=self.ACTION, category=record[0])
		row['uri1'] =  url.uri(action=self.ACTION, category=record[1])
		row['cat0'] =  record[0]
		row['cat1'] =  record[1]
		return row


class DbMixin(DataMixin):
	DATAMODEL = None
	TABLE=None
	
	TABLENAME = 'table'
	QS_TABLENAME = TABLENAME

	KEYNAME= "loginId"
	QS_KEYNAME= KEYNAME
	KEY=None

	
	def getField(self, handler, qs_key, key, default=None):
		value =  handler.req().getInput(qs_key)
		if not value:
			value = self.attrs.get(key, default)
		return value
		
		
	def getTable(self, handler):
		tabelname =  self.getField(handler, self.QS_TABLENAME, self.TABLENAME, self.TABLE)
		if tablename:
			return getattr(self.DATAMODEL, tablename)
		

	def getKey(self, handler):
		return self.getField(handler, self.QS_KEYNAME, self.KEYNAME, self.KEY)

	def getRecord(self, handler, key):
		table = self.getTable(handler)
		return datamodel.get(table, key)


	def getSelection(self, handler, selectCriteria): 
		cursor = datamodel.select(datamodel.Contractor, selectCriteria)
		return cursor
