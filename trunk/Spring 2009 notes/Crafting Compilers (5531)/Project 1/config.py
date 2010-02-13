#!-- This is a user-modifiable file (partially!) that will allow the user to configure
# different aspects of the scanner (the most important ones - which RE's to match,
# and which functions to call on each match.  parsing functions are in the
# parse_funcs library.

debug = True

#I may change these to const declarations but I may just leave them like this for now.
#these are the valid tokens that can be outputted by the parse functions.
toks = {
'ID':     251, 'INTCONST': 252, 'CHARCONST': 253, 'STRCONST': 254, #Major Stuff
'if':     255, 'else':     256, 'while':     257, 'int':      258, #Keywords
'string': 259, 'char':     260, 'return':    261, 'void':     262, #Keywords
'+' : 263, '-' : 264, '*' : 265, '/' : 266, '<': 267, '>': 268,    #OPs
'>=': 269, '<=': 270, '==': 271, '!=': 272, '=': 273,              #OPs
'[' : 274, ']' : 275, '{' : 276, '}' : 277, '(': 278, ')': 279,    #Brackets/Parens
',' : 280, ';' : 281                                               #Punctuation
} 

from parse_funcs import tokenize, sliteral, cliteral, iliteral, identifier, nothing
import re

# The way precedence works is that the first RE has higher relevance.
#therefore if the 'reserved word' RE matching "if" occurs before 'identifier' in the regexes list,
# then the string "if" will be matched to 'reserved word' not 'identifier.'

# the first item in each list is the RE that matches, the second is the function to be called to handle the match,
# and the third is optional parameters to the re.match function.
regexes = [['if|else|while|int|string|char|return|void', tokenize],               # keywords
           ['".*"', sliteral],                                                    #string literal
           ["'.'", cliteral],
           ["[1-9][0-9]*", iliteral],                                             #integer literal
           ["[A-Za-z][A-Za-z0-9]*", identifier],                                  #identifier
           ["\+|\-|\*|\/|\<|\>|\<=|\>=|==|!=|=|\[|\]|\(|\)|{|}|\,|\;", tokenize], #operators, brackets/parens, punctuation
           ["/\*.*?\*/", nothing, re.DOTALL], ["\s+", nothing]                    #whitespace & comments get thrown away 
           ]
           
#!-------------------------------------------!          
#!------  End user-modifiable Code!  --------!
#!-------------------------------------------!

# compile the regular expressions to speed them up, end up with a list of 2-tuples (re object, function to call).
temp = []
for regex in regexes:
    if len(regex) == 3:
        temp.append((re.compile(regex[0], regex[2]), regex[1]))
    else:
        temp.append((re.compile(regex[0]), regex[1]))
regexes = temp