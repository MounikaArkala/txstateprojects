import re, sys    
from config import regexes, toks, debug 


# This is the main file, it does the scanning and calls the callback function for whichever regular
# expression had the longest match.  If no regular expressions matched then it will print an invalid
# token error.

#keep track of our line / column numbers.

class Token(object):
    def __init__(self, type, value, lineno, tokindex, colno):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.tokindex = tokindex
        self.colno = colno
    def __repr__(self):
        return str((str(self.type), str(self.value), str(self.lineno), str(self.tokindex), str(self.colno)))

class Lexer(object):
    def __init__(self, data):
        self.data = data
        self.line =  1
        self.column = 1
        self.tokenindex = 0
    
    def token(self):
        return token_gen()
        
    def token_gen(self):
        
        while 1:
            #scan through all the input file.
            #longest match stores the longest matching regular expression.
            #we try to match all regexes and any time one matches longer than the others
            # it supercedes the other regex.
            longest_match = None
            
            if self.tokenindex == len(self.data):
                raise StopIteration
            
            for regex in regexes:
                match = regex[0].match(self.data[self.tokenindex:])
                if match:
                    if not longest_match:
                        longest_match = (match, regex)
                    elif match.end() > longest_match[0].end():
                        longest_match = (match, regex)
                  
            # there was no longest match, this is usually due to a syntax error in defining literals/constants.
            if not longest_match:
                if self.data[self.tokenindex] == "\"":
                    print "\nERROR: UNTERMINATED STRING CONSTANT at Line %s Column %s!\n" % (self.line, self.column)
                #elif self.data[self.tokenindex] == "0":
                #    print "\nERROR: INVALID INT LITERAL at Line %s Column %s!\n" % (self.line, self.column)
                elif self.data[self.tokenindex] == "'":
                    print "\nERROR: INVALID CHAR LITERAL at Line %s Column %s!\n" % (self.line, self.column)
                else:
                    print "\nERROR: ILLEGAL TOKEN %s at Line %s Column %s!\n" % (self.data[0], self.line, self.column)
                    
                #data = data[1:]
                
                self.tokenindex += 1
                continue
                
            #try:
            result = longest_match[1][1](longest_match[0].group())
            if result:
                if longest_match[0].group() == '/':                
                    #an unterminated comment will end up in here, because / and * are valid tokens unfortunately.
                    if self.data[self.tokenindex:self.tokenindex+2] == "/*":
                        print "\nERROR: UNTERMINATED COMMENT at Line %s Column %s!\n" % (self.line, self.column)
                    self.tokenindex += 2
                    #data = data[2:]
                    continue
                        
            #except:
            #    print "\nSomething went wrong somewhere.\n"
            
            #data = data[longest_match[0].end():] # truncate the just-found item from the list.
            self.tokenindex += longest_match[0].end()
            
            #advance our column and line numbers.
            temp = longest_match[0].group()
            temp = temp.split("\n")
            if len(temp) > 1:
                self.line += len(temp) - 1
                self.column = len(temp[-1]) + 1
            else:
                self.column += longest_match[0].end()
            
            #type, value, lineno, tokindex, colno
            try:
                yield Token(result[0], result[1], self.line, self.tokenindex, self.column)
            except TypeError:
                continue
            