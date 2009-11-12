#
#   pso.gui.py  - Python Service Objects
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
#   $Id: gui.py,v 1.2 2003/11/18 19:04:22 thanos Exp $
#
#
# created: 21/08/2002  Thanos Vassilakis
#
#

#

from pso.util import mkDict
# application imports
from util.cache  import EvalCache


class Bouncer:
	def render(self, parser, attr, cdata):
		if self.shouldBounce(parser, attr):
			return self.bounce(parser, attr, cdata)
		return ''

	def shouldBounce(self, parser, attr):
		return 0

	def bounce(self, parser, attr, cdata):
		return ''
	

	

class Link:
	def render(self, parser, attr, cdata):
		if self.isEnabled(parser, attr):
			return self.renderEnabled(parser, attr, cdata)
		else:
			return self.renderDisabled(parser, attr, cdata)

	def isEnabled(self, parser, attr):
		return 1

	def renderEnabled(self, parser, attr, cdata):
		return parser.handler.url.href(cdata, **attr)

	def renderDisabled(self, parser, attr, cdata):
		return '<font color="gray">%s</font>' % cdata


class Info:
	def render(self, parser, attr, cdata):
		if self.isEnabled(parser, attr):
			return self.renderInfo(parser, attr, cdata)
		return ''

	def isEnabled(self, parser, attr):
		return 1

	def renderInfo(self, parser, attr, cdata):
		return cdata


class List:
	def __init__(self):
		self.records=None
	def shouldShow(self, parser, attr) : return 1
	def getRecords(self, parser, attr): pass
	def processRecord(self, parser, attr, record, fields): pass
	def prepare(self, parser, attr): return {}
	def render(self, parser, attr, cdata): 
		if not self.shouldShow(parser, attr): return ''
		if self.records is None:
			self.records = self.sort(parser, attr)
		rowlen = len(self.records)
		fields = self.prepare(parser, attr)
		rows = map(self.processRow, self.records, rowlen*((parser,attr, cdata, fields),)) 
		del self.records[:]
		self.records = None
		return '\n'.join(rows)

	def sort(self, parser, attr):
		return self.getRecords(parser, attr)

	def processRow (self, record, params):
		parser, attr, cdata, fields = params
		#MING DEBUG 01-02-03
		return cdata % self.processRecord(parser, attr, record, fields)
		#return str(self.processRecord(parser, attr, record, fields))

	def tableMethods(celf):
		table = celf()
		return table.render
	tableMethods = classmethod(tableMethods)


	
class Table(List):
	PAGESZ='10'
	paged=0

	PAGER_HTML = """<table border="0" cellpadding="2" cellspacing="0" width="100%%"> <tr bgcolor="#FFFEF"> <td align='left' nowrap><strong><font color="gray" face="Helvetica,Helvetica"> %(legend)s  %(prev)s  %(next)s </font></strong></td><td align='right' nowrap>&nbsp;<strong></tr></table>"""
	def processPager(self, parser, attr, cdata):
		if self.records is None:
			self.records = self.sort(parser, attr)
		(legend, prev, next, self.records) = self.tabulate(parser, attr, self.records)	
		return mkDict(legend=legend, prev=prev, next=next)

	def pager(self, parser, attr, cdata):
		if not self.shouldShow(parser, attr): return ''
		if not cdata:
			html = self.PAGER_HTML
		return html %  self.processPager( parser, attr, cdata)
		

	def uri(self, parser, attr, label, **vars):
		tablename = attr.get('name','')
		url = parser.handler.url.copy()
		sort  = vars.get('sort')
		if sort is None:
			sort = 	parser.handler.getInput(tablename+'sort')
		if sort is not None:
			url[tablename+'sort'] = sort
		line  = vars.get('line')
		if not line:
			line = 	parser.handler.getInput(tablename+'line')
		if line:
			url[tablename+'line'] = line
		del url['delta']
		return '<a href="%s">%s</a>' % (url, label)
		
	def tabulate(self, parser, attr, records):
		numberlines = len(self.records)
		tablename = attr.get('name','')
		line = int(parser.handler.getInput(tablename+'line', value='1'))
		pagesz = int(parser.handler.getInput(tablename+'pageSize', value=self.PAGESZ))
		if line > numberlines:
			line=int(numberlines / pagesz)*pagesz + 1
		elif (line < 1):
			line=1
		numberpages = numberlines/ pagesz  + (numberlines % pagesz > 0)
		currentpage = line/ pagesz  + (line % pagesz > 0)
		if (line > (1+(currentpage-1)*pagesz)):
			prevpage = 1+(currentpage-1)*pagesz
			nextpage=prevpage+pagesz
		else:
			prevpage = line - pagesz
			nextpage=line + pagesz
		if prevpage < 0:
			prevpage = 0
		if nextpage > numberlines:
			nextpage = 0
		records =  records[int(line-1): int(line+pagesz-1)]
		if nextpage:
			nexturi = self.uri(parser, attr, 'next', line= nextpage)
		else:		
			nexturi = 'next'
		if prevpage:
			prevuri = self.uri(parser, attr, 'prev', line= prevpage) + ' |'
		else:		
			prevuri = 'prev |'
		if not numberpages:
			return 'no data', '','', []
		return ('%d of %d - ' % ( currentpage, numberpages)), prevuri, nexturi, records

	def tableMethods(celf):
		table = celf()
		return table.pager, table.render
	tableMethods = classmethod(tableMethods)

class SortedTable(Table):
	def sort(self, parser, attr):
		records = self.getRecords(parser, attr)
		records.sort()
		return  records


class SortableTable(Table):
	SORTFIELD = "sort"
	PAGEFIELD = "line"
	def __init__(self):
		List.__init__(self)

	def toggle(self, parser, attr, current, field):
		if abs(current)== field:
			return -current
		return field

	def columnHead(self, parser, attr, currentColumn, innerhtml, default, column):
		label, field = column
		field +=1
		field = self.toggle(parser, attr, currentColumn, field)
		return self.buildTitle(parser, attr, field, innerhtml %label)

	def buildTitle(self, parser, attr, field, label):
		return self.uri(parser, attr, label, sort=field)

	def getColumns(self, attr):
		columns = attr.get("columns")
		if columns:
			columns = EvalCache.eval(columns, self.GLOBALS)
		return columns
		

	def sortRow(self, parser, attr, html):
		if not self.shouldShow(parser, attr): return ''
		tablename = attr.get('name','')
		columns = self.getColumns(attr)
		if columns:
			innerHtml = attr.get("innehtml", "%s")
			default = EvalCache.eval(attr.get("default","1"), self.GLOBALS)
			currentField = parser.handler.getInput(tablename+'sort')
			if not currentField:
				currentField = default
			else:
				currentField = int(currentField)
			sortrow = [ self.columnHead(parser, attr, currentField, innerHtml, default, column) for column in columns]
			return html %   tuple(sortrow)
		return html
				
		

	def sort(self, parser, attr):
		tablename = attr.get('name','')
		records =  self.getRecords(parser, attr)
		column = parser.handler.getInput(tablename+'sort')
		if not column:
			column = self.getDefaultSort(parser.handler, attr)
		else:
			column = int(column)
		if column:
			records = sortTab(records, column)
		return records

	def getDefaultSort(self, handler, attr):
		value =  EvalCache.eval(attr.get("default","0"), self.GLOBALS)
		if value > 0:
			value +=1
		elif value < 0:
			value -=1
		return value

	

	def tableMethods(celf):
		table = celf()
		return table.pager, table.sortRow, table.render

	tableMethods = classmethod(tableMethods)
	
	
	
	
class Tab:
	def __init__(self, action, label):
		self.action, self.label = action, label

	def render(self, parser, attr, cdata=''):
		if self.isEnabled(parser):
			return self.renderEnabled(parser, attr, cdata)
		else:
			return self.renderDisabled(parser, attr, cdata)

	def renderEnabled(self, parser, attr, cdata):
		return parser.handler.url.href(self.getLabel(parser), action=self.action) 
	def renderDisabled(self, parser, attr, cdata):
		return self.getLabel(parser)
	def getLabel(self, parser):
		return self.label

	def isEnabled(self, parser):
		return parser.handler.getInput('action') != self.action

class TabBar:
	SPACER=  ' | '
	HTML="%s"
	def render(self, parser, attr, cdata=''):
		if not cdata:
			cdata = self.HTML
		try:
			bar = self.getBar(parser, attr)
			spacer = attr.setdefault('spacer', self.SPACER)
			if bar:
				tabs = [tab.render(parser, attr, cdata) for tab in self.TABS.get(bar, ())]
				return cdata % spacer.join(tabs)
			return ''
		except Exception,e:
			print "<!--"
			import sys
			import traceback
			traceback.print_exc(file=sys.stdout)
			return str(e)
			print "-->"
			
			

	def getBar(self, parser, attr): pass

