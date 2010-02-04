import re, sys
tokendefs = {
'ID':     251, 'INTCONST': 252, 'CHARCONST': 253, 'STRCONST': 254, #Major Stuff
'if':     255, 'else':     256, 'while':     257, 'int':      258, #Keywords
'string': 259, 'char':     260, 'return':    261, 'void':     262, #Keywords
'+' : 263, '-' : 264, '*' : 265, '/' : 266, '<': 267, '>': 268,    #OPs
'>=': 269, '<=': 270, '==': 271, '!=': 272, '=': 273,              #OPs
'[' : 274, ']' : 275, '{' : 276, '}' : 277, '(': 278, ')': 279,    #Brackets/Parens
',' : 280, ';' : 281                                               #Punctuation
} 

def tokenize(value): # used for operators, punctuation, parens/brackets, and keywords.
    return str(tokendefs[value]) + "|"    
def sliteral(value): #used for string literals
    return str(tokendefs["STRCONST"]) + " " + value.strip("\"") + "|"
def iliteral(value): #used for integer literals
    return str(tokendefs["INTCONST"]) + " " + value + "|"
    

def identifier(value): # used for identifiers
    return str(tokendefs["ID"]) + " " + value + "|"
def nothing(value):
    return ""        
    
    
#TODO: match string "   \" " correctly.
        
# The way precedence works is that the first RE has higher relevance.
#therefore if the 'reserved word' RE matching "if" occurs before 'identifier' in the regexes list,
# then the string "if" will be matched to 'reserved word' not 'identifier.'
regexes = [['if|else|while|int|string|char|return|void', tokenize],               # keywords
           ["\".*\"", sliteral],                                                  #string literal
           ["[0-9]+", iliteral],                                                  #integer literal
           ["[A-Za-z][A-Za-z0-9]*", identifier],                                  #identifier
           ["\+|\-|\*|\/|\<|\>|\<=|\>=|==|!=|=|\[|\]|\(|\)|{|}|\,|\;", tokenize], #operators, brackets/parens, punctuation
           ["/\*.*?\*/", nothing, re.DOTALL], ["\s+", nothing]                    #whitespace & comments get thrown away 
           ]
for regex in regexes: regex[0] = re.compile(regex[0]) # compile the regular expressions to speed them up.

input_txt = open('test.c').read()
print "--------------------------"
print input_txt
print "--------------------------"
while 1:
    if len(input_txt) == 0:
        break
    longest_match = None
    for regex in regexes:
        if len(regex) == 3:
            match = regex[0].match(input_txt, regex[2])
        else:
            match = regex[0].match(input_txt)
        if match:
            if not longest_match:
                longest_match = (match, regex)
            elif match.end() > longest_match[0].end():
                longest_match = (match, regex)
            
    if not longest_match:
        print "token mismatch, consuming ", input_txt[0],"." # TODO: this should be an error.
        input_txt = input_txt[1:]
        continue
    try:
        sys.stdout.write(longest_match[1][1](longest_match[0].group()))
    except:
        print "Something went wrong somewhere..."
    input_txt = input_txt[longest_match[0].end():] # truncate the just-found item from the list.