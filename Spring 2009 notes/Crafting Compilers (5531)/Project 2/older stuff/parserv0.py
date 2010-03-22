# ------------------------------------------------------------
# 
# ------------------------------------------------------------
#import ply.lex as lex


"""
import sys



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


#lexer.input(data)

import mylex.lex as mylex

lexer = mylex.Lexer(input_txt)



    
    
    
    
    
    
    
    
    
tokens = (
    'NAME','NUMBER',
    )

literals = ['=','+','-','*','/', '(',')']


# Parsing rules

precedence = (
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

        
        
        
import ply.yacc as yacc
yacc.yacc()







    # Tokenize
    #for tok in lexer.token_gen():
    #    print tok
yacc.parse(lexer.token_gen())

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
"""



import sys
data = open(sys.argv[1]).read()


   
import ply.lex as lex


"""
# Compute column.  Helper function to find column # from a token.
#     input is the input text string
#     token is a token instance
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
	last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column
"""




# List of token names.   This is always required
tokens = (
   'INT_LITERAL',
   'CHAR_LITERAL',
   'STRING_LITERAL',
   #keywords
   'IF',
   'ELSE',
   'WHILE',
   'RETURN',
   'VOID',
   'INT',
   'CHAR',
   'STRING',
   'IDENTIFIER',
   #operators
   'PLUS',
   'MINUS',
   'DIVIDE',
   'MULTIPLY',
   'LESS',
   'GREATER',
   'LTE',
   'GTE',
   'EQ',
   'NEQ',
   'ASSIGN',
   #braces
   'RBRACKET',
   'LBRACKET',
   'RPAREN',
   'LPAREN',
   'RBRACE',
   'LBRACE',
   #misc
   'COMMA',
   'SEMICOLON'
)
ops = {'+' : 'PLUS', '-' : 'MINUS', '*' : 'MULTIPLY', '/' : 'DIVIDE', '<': 'LESS', '>': 'GREATER',    #OPs
'>=': 'GTE', '<=': 'LTE', '==': 'EQ', '!=': 'NEQ', '=': 'ASSIGN',              #OPs
'[' : 'LBRACKET', ']' : 'RBRACKET', '{' : 'LBRACE', '}' : 'RBRACE', '(': 'LPAREN', ')': 'RPAREN',    #Brackets/Parens
',' : 'COMMA', ';' : 'SEMICOLON'}                                               #Punctuation

kwds = {'if': 'IF', 'else': 'ELSE', 'while': 'WHILE', 'int': 'INT', 'string': 'STRING', 'char': 'CHAR', 'return': 'RETURN', 'void': 'VOID'}
#All the tokens that don't require functions.
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_INT = r'int'
t_STRING = r'string'
t_CHAR = r'char'
t_RETURN = r'return'
t_VOID = r'void'

def t_IDENTIFIER(t):
    r'[A-Za-z][A-Za-z0-9]*'
    if t.value in kwds.keys():
        t.type = kwds[t.value]
    return t

def t_CHAR_LITERAL(t):
    r"'.'"
    t.value = t.value.strip("'")
    return t

def t_OPS(t):
    r"\+|\-|\*|\/|\<|\>|\<=|\>=|==|!=|=|\[|\]|\(|\)|{|}|\,|\;"
    t.type = ops[t.value]
    return t
    
def t_STRING_LITERAL(t):
    r'".*"'
    value = t.value
    value = value[1:-1]
    
    #now we need to make sure this is a valid string literal.
    strpieces = []
    while value != "":
        loc = value.find("\\")
        if loc != -1:
            strpieces.append(value[:loc])
            try:
                follower = value[loc+1]
                if follower == "t":
                    strpieces.append("\t")
                elif follower == "n":
                    strpieces.append("\n")
                elif follower == '"':
                    strpieces.append("\"")
                elif follower == "\\":
                    strpieces.append("\\")
                else:
                    #unknown value
                    print "\nERROR: unknown escape sequence \%s in string literal.\n" % value[loc+1]
            except:
                print "\nERROR: string literal ends with an incomplete escape sequence (single '\\').\n"

            value = value[loc+2:]
        else:
            strpieces.append(value) #just use the rest of val.
            value = ""
    value = "".join(strpieces)
    t.value = value
    return t
    
    

#Rules that just consume but don't return tokens:
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_comments(t):
    r'/\*.*?\*/'
    #don't return a value.
    
    
    
    
#Rules that perform a mutation function before returning token
def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)    
    return t
    
    
    


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    #if the first character is a " then we have an unterminate string constant.
    if t.value[0] == '"':
        print "Unterminated String Constant at Line %s Column %s" % (t.lineno, find_column(data, t))
        #print t
        
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

    
#------------- end of lexer stuff.


class Node(object):
    def __init__(self,nodetype,*kwargs):
        self.type = nodetype
        self.children = []
        for item in kwargs:
            #if it's not already a node, add it as a leaf node.  a leaf node is just a node w/ no children (default).
            if type(item) != type(self):
                self.children.append(Node(item))
            #otherwise add it directly.
            else:
                self.children.append(item)
                
    
    
import ply.yacc as yacc
    
    
scope = "global"
identifiers = {"global": [], "local": []}


def p_start(p):
    'program : varDecl stmt SEMICOLON'
    p[0] = Node("program", p[1], p[2], p[3])

def p_varDecl(p):
    '''varDecl  : typeSpecifier IDENTIFIER'''
    p[0] = Node("varDecl", p[1], p[2])
    
def p_stmt(p):
    '''stmt : assignStmt
            | ifStmt'''
    p[0] = Node("stmt", p[1])
    
def p_assignStmt(p):
    ''' assignStmt : var ASSIGN exp'''
    p[0] = Node("assignStmt", p[1], p[2], p[3])

def p_ifStmt(p):
    '''ifStmt : IF LPAREN exp RPAREN stmt
              | IF LPAREN exp RPAREN stmt ELSE stmt'''
    if len(p) > 6:
        p[0] = Node("ifStmt", p[1],p[2],p[3],p[4],p[5],p[6],p[7])
    else:    
        p[0] = Node("ifStmt", p[1],p[2],p[3],p[4],p[5])

def p_exp(p):
    '''exp : empty
           | INT_LITERAL
           | IDENTIFIER'''
    p[0] = Node("exp", p[1])

def p_var(p):
    '''var : IDENTIFIER'''
    p[0] = Node("var", p[1])
    
def p_typeSpecifier(p):
    '''typeSpecifier : INT
                     | CHAR
                     | VOID'''
    p[0] = Node("typeSpecifier", p[1])
    
    
# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    print p

#lets us have empty productions.
def p_empty(p):
    'empty :'
    pass


# Build the lexer
lexer = lex.lex()

# Give the lexer some input
lexer.input(data)

# Build the parser
parser = yacc.yacc(debug=True)
    
    
# Tokenize
#for tok in lexer:
#    print tok
    
result = parser.parse(data)


#draw the graph...

import pydot, random



def makeGraph(graph, tree, parent=None, val=0):
    #take a graph and node as input.
    #attach the node to the graph, then attach all children as subgraphs,
    #then attach all leafs as nodes.
    print "graph: ", graph.get_name()
    print "node: ", tree.type
    # make a subgraph
    node = pydot.Node(name=str(val), label=tree.type)
    graph.add_node(node)
    val += 1
    
    if parent != None:
        graph.add_edge(pydot.Edge(parent, node))
        
    #recurse for subtrees
    for subtree in tree.children:
        val = makeGraph(graph, subtree, node, val)
    
    return val


print "graph drawing..."        
      
graph = pydot.Dot(graph_type='digraph')  
makeGraph(graph, result)
graph.set_graphviz_executables(paths={'dot': r'C:\Program Files (x86)\Graphviz2.26.3\bin\dot.exe'})
graph.write_svg('graph_dot.svg', prog='dot')

print "graph drawn."

print "identifiers defined: ", identifiers