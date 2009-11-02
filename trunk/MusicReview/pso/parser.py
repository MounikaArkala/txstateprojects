"""
#
#   pso.parser.py  - Python Service Objects Parser
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
#   $Id: parser.py,v 1.18 2004/07/12 04:04:43 thanos Exp $
#


SYNOPSIS

Senario One

First you make a template - this is just a normal HTML file with a few extra tags:

For example, test.tmpl:

  <HTML>
  <BODY>
  My Email: <pso pso=mypanel:Email>thanos@0x01.com</pso.py>
  <P>
  My Name: <pso pso=mypanel:Name  src="http://www.0x01.com/" name="Thanos Vassilakis" />
  </BODY>
  </HTML>
Now create the mypanel package, mypanel.py

from pso.parser import Tag


class Email(Tag):
    "renders email as a uri"
    def render(self, cdata):
        return '<a href="mailto:%s">%s</a>' % ( cdata, cdata)

class Name(Tag):
    "renders name as a uri"
    def render(self, cdata=''):
        return '<a href="%(src)s">%(name)s</a>' % self.getAttrs()

Save it in the python path.

Now write the script:

from pso.parser import Parser
psoParser = Parser()
psoTree = psoParser.parseFile("test.tmpl")
print psoTree.render()

Running this script should generate: 

  <HTML>
  <BODY>
  My Email: <a href="mailto:thanos@0x01.com">thanos@0x01.com</a>
  <P>
  My Name: <a href="http://www.0x01.com/">Thanos Vassilakis</a>
  </BODY>
  </HTML>

  



Senario Two

Now you might want to just extract the tags and document them...

class TagDocumentor:
    def document(self, object, cdata=''):
        if object:
            self.documentation  += '\t<td>%s</td><dd>%s<dd><br>\n' % (object.__class__, object.__class__.__doc__)
            
    def do(self, infile):
        self.documentation =''
        psoParser = Parser()
        psoTree = psoParser.parseFile(infile, noCache=1)
        psoTree.render(self.document)
        print "<dl>%s</dl>"

TagDocumentor().do(test.tmpl)

And you will get:

<dl>
    <td>mypanel.Email</td><dd>renders email as a uri</dd>
    <td>mypanel.Name</td><dd>renders name as a uri</dd>
</dl>

Senario Three 

You want to write a robot (this is simplistic - beware):

class a(Tag):
	def getUrl(self, cdata):
		return self.getAttrs()['href'], cdata

class A(a): pass


class Robot:
    def process(self, object, cdata=''):
        if object:
		url, linkText = object.getUrl(cdata)
		if url not in self.links:
			self.links[url] = linkText
			self.do(url)
            
	def do(self, url):
		psoParser = Parser()
		psoTree = psoParser.parseFile(self.getPage(url),  allTags=1) 
		psoTree.render(self.process)

	def run(self, startUrl):
		self.links = {}
		self.do(startUrl)
		for url, linkText in self.link.items():
			print '<a href="%s">%s</a>'   % (url, linkText)

"""



__version__="$Revision: 1.18 $"

__all__ =["Tag", "Parser", "CachedParser"]

from types import *
from time import time
from string import letters, digits, whitespace
from os.path import split, join, exists
from stat import ST_MTIME
from statcache import stat, forget
from cPickle import dump, load
from copy import copy
import traceback
import sys


from util import log

from table import CIMap

silent=1

class PSOParts:
    def __init__(self, parent=None, name ='', className='', start=0, end=0, text='', attribute=None):
        self.setup(parent, name, className, start, end, text, attribute)
        self.children=[]
	self.attribute=attribute
        
    def setup(self, parent, name, className, start, end, text, attribute):
        self.parent = parent
        self.name  = name
        self.className= className
        self.text = text
        self.start = start
        self.end =  end
	self.attribute = attribute

def psoSetup(object, parent, name, className, start, end, text, attribute):
        if isinstance(object, PSO):
            object.psoParts.setup(parent, name, className, start, end, text, attribute)
        else:
            object.psoParts = PSOParts(parent, name, className, start, end, text, attribute)





class PSO:    
    def __init__(self, **kw):
            """
		@param kw: the kew word argumenst match the tags set attributes
            """
            self.attrs= CIMap(kw)
            self.init()
            self.psoParts=PSOParts()


    def init(self): 
            """
		Overide to setup the tags values.
            """

    def getAttrs(self): return self.attrs

    
    def setup(self, parent, name, start, end, text):
            """
		Sets up a tag with its:
		@param name: the tags name. <A> has name="A"
		@param start: character start position of tag in template.
		@param end: character end position of tag in template.
		@param text: the actuals tags text n the template before rendering.
            """
            self.psoParts = PSOParts(parent, name, start, end, text)

    def getChildren(self):
            """
		@return a list of the tags  nested within this one.A
            """
            return self.psoParts.children

    def append(self, child):
        children  = self.psoParts.children
        if children and type(children[-1]) is StringType and  type(child) is StringType:
            children[-1] += child
        else:
            children.append(child)

    def preProcess(self, renderer=None): 
            """
		Called before renderer has visited the nested tags. Overirde this method when 
		you need to do validation before the nested tags are rendered.
            """
            return ''
		
	
    def travers(self, renderer=None):
	result = self.preProcess(renderer.im_self)
        try:
            for child in self.psoParts.children:
                if type(child) is StringType:
                    retval = renderer(None, child)
                else:
                    retval = str(child.travers( renderer))
                if retval:
                    result +=retval
            if self.psoParts.parent:
                result = renderer(self,  result)
        except Exception, e:
            try:
                result= ("%s: %s\n<!-- %s --->\n" % (self.psoParts.name ,e, "\n".join(traceback.format_exception( *sys.exc_info()))))
	    except:
		result = ("%s\n<!-- %s --->\n" % (e, "\n".join(traceback.format_exception( *sys.exc_info()))))
        return result

        


		
class PSOTree(PSO):		
	def renderer(self, object, cdata=''):
		if not object:
			return cdata
			
                return object.render(self, cdata)

	def render(self,  renderer = None):
		if not renderer:
			renderer = self.renderer
		return self.travers( renderer)
		
    
       

class Token:pass
class CData: pass
class Comment: pass
class StartTag(Token): pass
class SingleTag(Token): pass
class EndTag(Token): posstart=2



def getName(text, start=1, oldname=''):
    
    if oldname:
        return oldname
    text = text[start:]
    ind = text.find(' ')
    if ind > -1:
        name=text[:ind]
    else:
        if '/' in text:
            name = text[:-2]
        else:
            name=text[:-1]
    return name

firstKeyChar = letters + digits+'_'
keyChars = letters + digits+'_.-'

def getAttrs(attrs):
	ind = attrs.find(' ')
        if ind > -1 and len(attrs) - ind > 2:
            attrs = attrs[ind:-1]
        else:
            return {}
        
	dict ={}
	if not attrs:
	    return dict
        state='start'
	while attrs:
		ch = attrs[0]
		attrs=attrs[1:]
		if state == 'start':
			key=value=''
			if ch in whitespace:
				continue
			if ch in firstKeyChar:
				state='key'
				key += ch
		elif state =='key':
			if ch in keyChars:
				state='key'
				key += ch
			elif ch in whitespace:
				state= '='
			elif ch ==  '=':
				state= 'value'
				delim=''
		elif state =='=':
			if ch in whitespace:
				continue
			elif ch ==  '=':
				state='value'
				delim=''
			elif ch not in whitespace:
				dict[key]=''
				state='start'
				attrs = ch + attrs
		elif state =='value':
			if not delim:
				if ch in '"\'':
					delim = ch
				elif ch not in whitespace:
					delim = whitespace
					value +=ch
			else:
				if ch in delim:
					dict[key] = value
					state='start'
				else:
					value +=ch
	else:
		if key:
			dict[key] = value
			
        return dict		

class Tag(PSO):
	def processAttrs(self,  **kws):
		attrs={}
		for k,v in self.getAttrs().items():
			attrs[k] = v
		for k,v in kws.items():
			attrs[k] = v
		return attrs

	def buildAttrList(self,  attrs):
		list = ""
		for k,v in  attrs.items():
			if k =='tagname':
				continue
			if v is None:
				list = "%s %s" % ( list, k)
			elif '"' in str(v):
				list = "%s %s='%s'" % ( list, k, v)
			else:
				list = '%s %s="%s"' % ( list, k, v)
		return list
				
	def buildAttrs(self,  **kws):
		return self.buildAttrList( self.processAttrs( **kws ))




			
		
	def render(self, renderer, cdata=''):
		if self.psoParts.attribute:
			return getattr(self, self.psoParts.attribute)(renderer, cdata)
		return self(renderer, cdata)

	def __call__(self, renderer, cdata=''):
		"""
		Override to render tag. Here is where everything happens!
		"""
		return cdata

class PSOTag(Tag):pass 
    
class Tokenizer:
    TagToFind=0
    PsoTagFound=1
    TagFound =2
    TagStart=3
    
    
    
    def __init__(self, text, allTags=0):
        self.text = text
        self.allTags= allTags
        self.textLength= len(self.text)
        self.reset()
        

    def reset(self):
        self.state=self.TagToFind
        self.index=0

        
    def getToken2(self, defaultModule, reject={}, accept={}):
            blockstart = self.index
            rejectTag = 0
            while  self.index < self.textLength:
                try:
                    if self.state is self.TagToFind:
                        self.index = self.text.index('<', self.index)
                        ch1 = self.text[self.index+1]
                        if ch1 == '/':
                            dif = 1
                            ch1 = self.text[self.index+dif+1]
                        else:
                            dif = 0
                        if ch1 == 'p'or ch1=='P':
                            ch2=self.text[self.index+dif+2]
                            if ch2 == 's'or ch2=='S':
                                ch3=self.text[self.index+dif+3]
                                if ch3 == 'o'or ch3=='o':
                                    self.state = self.PsoTagFound
                                    return CData, '', blockstart, self.index, self.text[blockstart:self.index]
                        if self.allTags and ch1 != '!':
                            self.state = self.TagFound
                            return CData, '', blockstart, self.index, self.text[blockstart:self.index]
 
                        self.index = self.text.index('>', self.index+1)+1
                    elif self.state in (self.PsoTagFound, self.TagFound):
                        tagstart = self.index 
                        self.index = self.text.index('>', tagstart)+1
                        text = self.text[tagstart:self.index]
                        if text[-2] =='/':
                            tag, startpos = SingleTag, 1    
                        elif text[1] =='/':
                            tag, startpos = EndTag,2        
                        else:
                            tag, startpos = StartTag,1
                        if self.state == self.PsoTagFound:
                            if tag is not EndTag:
                                attrs = getAttrs(text)
                            else:
                                attrs= {'pso':'pso'}
                        else:
                            name = getName(text, startpos)
                            if name.find(':') < 0:
                                if defaultModule:
                                    name = defaultModule+':'+name
                                else:
                                    rejectTag = 1
                            attrs= {'pso':name}
                        if not rejectTag and not reject.has_key(attrs['pso']):
                                return tag, attrs, tagstart, self.index, text
                        self.state = self.TagToFind
                        rejectTag =0
                        
                except ValueError:
                        start= blockstart
                        self.state=self.TagToFind
                        self.index = len(self.text)
                        return CData, '', start, self.index, self.text[start:self.index]
            return None, '', 0, 0, ''
                    
       
    def getToken(self, defaultModule, reject={}, accept={}):
        blockstart = self.index
        while  self.index < self.textLength:
            try:
                if self.state is self.TagToFind:
                    self.index = self.text.index('<', self.index)
                    if self.text[self.index+1] !='!':
                        self.state = self.TagFound
                        return CData, '', blockstart, self.index, self.text[blockstart:self.index]
                    self.index = self.text.index('>', self.index+1)+1
                elif self.state is self.TagFound:
                    tagstart = self.index 
                    self.index = self.text.index('>', tagstart)+1
                    self.state = self.TagToFind
                    text = self.text[tagstart:self.index]
                    if text[-2] =='/':
                        tag, startpos = SingleTag, 1    
                    elif text[1] =='/':
                        tag, startpos = EndTag,2        
                    else:
                        tag, startpos = StartTag,1
                    name = getName(text, startpos)
                    attrs={}
                    if name =='pso' or name =='/pso':
                        attrs  = {'tagname':'pso', 'pso':name}
                        attrs.update(getAttrs(text))
                    else:
                        attrs = {'tagname':name, 'pso':name}
                        attrs.update(getAttrs(text))
                    if not reject.has_key(name):
                        return tag, attrs, tagstart, self.index, text
            except ValueError:
                start= blockstart
                self.state=self.TagToFind
                self.index = len(self.text)
                return CData, '', start, self.index, self.text[start:self.index]
        return None, '', 0, 0, ''
   

    
def PSOimport(module, object=None, doReload=0):
    try:
        if not object:
            mod = __import__(module)
            if doReload:
                reload(mod)
            comps = name.split('.')
            for c in comps[1:]:
                    mod = getattr(mod, c)
            obj = mod
        else:
            m = __import__(module, globals(), locals(), [object,])
            if doReload:
                reload(m)
            obj =  getattr(m, object)
        return obj
    except:
        if not silent:
            import traceback
            traceback.print_exc()

       
class Parser:
    """
	pso.Parser(defaultModule) - Creates a new parser. The default module is the actual parser module unless its given. 
	When a parser is created with  pso.Parser("mytags") tags such as <pso pso="Login" /> or <Login /> will be treated as if they were writen <pso pso=mytags:Login /> or <mytags:Login />.
    """
	
    sShared={}
    def __init__(self, defaultModule=""):
        self.tokenTree=PSOTree()
        self.sTagsAccepted={}
        self.sTagsRejected={}
        self.defaultModule =defaultModule

    def clear(self):
            self.sTagsAccepted={}
            self.sTagsRejected={}
            self.__class__.sShared={}

    

    def parseFile(self, filePath, oPath='', noCache=1, reload=0, allTags=0):
        
	if noCache:
                f = open(filePath)
                self.parse(f.read(), reload, allTags)
	else:
		ttime = stat(filePath)[ST_MTIME]
		if oPath:
		    path, file = split(filePath)
		    ofilePath= join(oPath, file)
		else:
		    idx = filePath.rindex('.')
		    if idx > -1:
			ofilePath= filePath[:idx] + '.pso'
		    else:
			ofilePath = filePath+'.pso'
		    try:
			
			otime = stat(ofilePath)[ST_MTIME]
			if otime < ttime:
			    raise 'do parse'
			tagsAccepted, tagsRejected, self.tokenTree = load(open(ofilePath))
			self.sTagsAccepted.update(tagsAccepted)
			self.sTagsRejected.update(tagsRejected)
		    except:
                        if not silent:
                            import traceback
                            traceback.print_exc()
			f = open(filePath)
			self.parse(f.read(), reload, allTags)
			if not noCache:
			    dump((self.sTagsAccepted, self.sTagsRejected, self.tokenTree), open(ofilePath,'wb'))
			forget(ofilePath)
		    forget(filePath)
        return self.tokenTree
		    
            
                
    def parse(self, text, reload=0, allTags=0):
        self.reload= reload
        self.tokenizer = Tokenizer(text, allTags)
        return self.processNode(self.tokenTree)
        
    
    def getPSO(self, parent, args):
        tag, attrs, start, end, text = args
        className = attrs['pso']
	attribute=None
        if self.sTagsRejected.has_key(className):
            return text
        renderer = None
        if  self.sTagsAccepted.has_key(className):
                renderer, attribute= self.sTagsAccepted[className]
                #return renderer
        else:
            renderer, attribute = self.findObject(className)
        if renderer:
            objectType = type(renderer)
            if objectType is ClassType:
                if len(attrs) == 1:
                    attrs.update(getAttrs(text))
                whatToSave = renderer, attribute
                renderer = renderer(**attrs)
                psoSetup(renderer, parent, attrs['tagname'], className, start, end, text, attribute)
                self.sTagsAccepted[className] = whatToSave
            elif objectType is not StringType:
                renderer = str(renderer)
                whatToSave= renderer, None
                self.sTagsAccepted[className] = whatToSave
            return renderer
        else:
            self.sTagsRejected[className]=None
            tag = None
        return text
    

    def findObject(self, tagName):
        objName=''
        moduleName=''
        if hasattr(self, '%s' % tagName):
            return getattr(self, 'tag_%s' % tagName), None
        elif hasattr(self, 'tag_%s' % tagName):
            return getattr(self, 'tag_%s' % tagName), None
        elif globals().has_key(tagName):
            return globals()[tagName], None
        #elif tagName in dir(__builtins__):
        #    return getattr(__builtins__, tagName)
        else:
            indx = tagName.find(':')
	    if indx > -1:
                moduleName = tagName[:indx]
                objName = tagName[indx+1:]      
            elif self.defaultModule:
                moduleName = self.defaultModule
                objName = tagName
                tagName = moduleName+':'+objName
        if objName:
            indx = objName.find('.')
            if indx > -1:
                attribute = objName[indx+1:]
                objName = objName[:indx]
                return PSOimport(moduleName, objName, doReload= self.reload), attribute
            else:
                return PSOimport(moduleName, objName, doReload= self.reload), None
        return None, None

    def processNode(self, currentNode):
        doAppend = currentNode.append
        cAppend = currentNode.getChildren().append
        getToken = self.tokenizer.getToken
        tagRejected = self.sTagsRejected
        tagsAccepted = self.sTagsAccepted
        while 1:
            token, attrs, start, end, text = getToken(  self.defaultModule, self.sTagsRejected, self.sTagsAccepted)
            if not token:
                return currentNode
            if token is CData:
                doAppend(text)      
            elif token is StartTag:
                node = self.getPSO(currentNode, (StartTag, attrs, start, end, text))
                if type(node) is StringType:
                        doAppend(node)
                else:
                    cAppend(self.processNode(node))
            elif token is SingleTag:
                node = self.getPSO(currentNode, (SingleTag, attrs, start, end, text))
                if type(node) is StringType:
                    doAppend(node)
                else:
                    cAppend(node)
            elif token is EndTag:
                if hasattr(currentNode,'psoParts'): 
                    tokenName = currentNode.psoParts.name
                    if currentNode.psoParts.name  == attrs['tagname']:
                        break
                doAppend(text)
            else:
                doAppend(text)
        return currentNode
        

class CachedParser(Parser): 
	trees={}
	def parseFile(self, filePath, oPath=''):
		tree = self.trees.get(filePath)
		if not tree:
			tree = Parser.parseFile(self, filePath, oPath)
			self.trees[filePath] = tree
		return tree

class PSOParser(Parser):pass 


if __name__ =='__main__':
    file1 = 'templates/contractor_detail1.html'
    print '-'*25
    class TagDocumentor:
        def render(self, object, cdata=''):
            if object:
                self.documentation  += ("""<td>%s</td><dd>%s<dd><br>\n""" % (object.__class__, object.__class__.__doc__))
            
        def do(self, infile, outfile):
            self.documentation =''
            psoParser = Parser()
            psoTree = psoParser.parseFile(infile, noCache=1)
            psoTree.render(self.render)
            open(outfile, 'w').write("<dl>%s</dl>" % self.documentation)

    class TagIndexer:
        index = 0
        def render(self, object, cdata=''):
                if object:
                    self.index +=1
                    index = self.index
                    
                    if cdata:
                        return ":<%s>%s</%s>:" % (index, cdata, index)
                    return ":<%s />:" % index
                return cdata
            
        def do(self, infile, outfile):
            self.index =0
            psoParser = Parser()
            psoTree = psoParser.parseFile(infile, )
            open(outfile, 'w').write(psoTree.render(self.render))

    import time
        
    class TagTimer:
        def timer(self, object, cdata=''):
            if object:
                t = time.time()
                r = self.render(object, cdata)
                self.tagTimes[object.__class__.__name__] = time.time() - t
                return r
            return self.render(object, cdata)
            
        def do(self, infile):
            self.tagTimes={}
            psoParser = Parser()
            psoTree = psoParser.parseFile(infile)
            print psoTree.render(self.timer)
            for k,v in self.tagTimes.items():
                print k, v

    class IndexerTimer(TagTimer, TagIndexer): pass

    try:
        import sys
        infile = file1 #sys.argv[1]
        outfile = 'r3' #sys.argv[2]
        TagIndexer().do(infile, 'r2')
        TagDocumentor().do(infile, 'r3')
        IndexerTimer().do(infile)
    except Exception,e:
        print e
        print """
        usage parser.py template_file output_file
        """
        
