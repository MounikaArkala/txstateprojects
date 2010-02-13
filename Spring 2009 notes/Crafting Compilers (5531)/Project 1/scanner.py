import re, sys    
from config import regexes, toks, debug 
# This is the main file, it does the scanning and calls the callback function for whichever regular
# expression had the longest match.  If no regular expressions matched then it will print an invalid
# token error.
 
try:
    fname = sys.argv[1]
except:
    print 'Invalid Usage: type "python %s filename" (without quotes) to run program "filename".' % sys.argv[0]
    print "example: python %s test.c" % sys.argv[0]
    raise SystemExit
    
input_txt = open(fname).read()
print "this is your input text: "
print "--------------------------"
print input_txt
print "--------------------------"
#keep track of our line / column numbers.
line = 1
column = 1
while input_txt: #scan through all the input file.
    #longest match stores the longest matching regular expression.
    #we try to match all regexes and any time one matches longer than the others
    # it supercedes the other regex.
    longest_match = None
    for regex in regexes:
        match = regex[0].match(input_txt)
        if match:
            if not longest_match:
                longest_match = (match, regex)
            elif match.end() > longest_match[0].end():
                longest_match = (match, regex)
          
    # there was no longest match, this is usually due to a syntax error in defining literals/constants.
    if not longest_match:
        if input_txt[0] == "\"":
            print "\nERROR: UNTERMINATED STRING CONSTANT at Line %s Column %s!\n" % (line, column)
        elif input_txt[0] == "0":
            print "\nERRROR: INVALID INT LITERAL at Line %s Column %s!\n" % (line, column)
        elif input_txt[0] == "'":
            print "\nERRROR: INVALID CHAR LITERAL at Line %s Column %s!\n" % (line, column)
        else:
            print "\nERROR: ILLEGAL TOKEN %s at Line %s Column %s!\n" % (input_txt[0], line, column)
            
        input_txt = input_txt[1:]
        continue
        
    try:
        result = longest_match[1][1](longest_match[0].group())
        if result:
            if longest_match[0].group() == '/':                
                #an unterminated comment will end up in here, because / and * are valid tokens unfortunately.
                if input_txt[0:2] == "/*":
                    print "\nERROR: UNTERMINATED COMMENT at Line %s Column %s!\n" % (line, column)
                
                input_txt = input_txt[2:]
                continue
                
            print result
    except:
        print "\nSomething went wrong somewhere... crap.  not sure.\n"
    input_txt = input_txt[longest_match[0].end():] # truncate the just-found item from the list.
    
    #advance our column and line numbers.
    temp = longest_match[0].group()
    temp = temp.split("\n")
    if len(temp) > 1:
        line += len(temp) - 1
        column = len(temp[-1]) + 1
    else:
        column += longest_match[0].end()