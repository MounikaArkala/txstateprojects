# ------------------------------------------------------------
# mcc.py by Luke Paireepinart, Texas State University, Spring 2010
# 
# This is a lexical analyzer and parser for the mC language specification.
# it outputs a .svg file of the abstract syntax tree.
# this is the second part of a multi-part assignment,
# so the AST will be utilized more extensively in the coming assignments.
# ------------------------------------------------------------

import sys, re
from libs.ply import lex as lex

#Change the dotpath to the place where your dot executable is.
dotpath = r'C:\Program Files\Graphviz2.26.3\bin\dot.exe'
#change this if you'd like to see a few debug statements (there aren't many.)
DEBUG = False

#keep track of errors.
syntaxerrs = 0
lexerrs = 0

if len(sys.argv) != 3:
    print "Usage: python %s data_in.c graph_out.svg" % sys.argv[0]
    raise SystemExit

data = open(sys.argv[1]).read()
graph_out = sys.argv[2]

# Compute column.  Helper function to find column # from a token.
#     input is the input text string
#     token is a token instance
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
	last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column


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

#The tokens below are all the tokens that don't require functions.
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_INT = r'int'
t_STRING = r'string'
t_CHAR = r'char'
t_RETURN = r'return'
t_VOID = r'void'

#now are the tokens that require functions.
def t_IDENTIFIER(t):
    r'[A-Za-z][A-Za-z0-9]*'
    #reserved words.
    kwds = {'if': 'IF', 'else': 'ELSE', 'while': 'WHILE', 'int': 'INT',
            'string': 'STRING', 'char': 'CHAR', 'return': 'RETURN', 'void': 'VOID'}
    if t.value in kwds.keys():
        t.type = kwds[t.value]
    return t

def t_CHAR_LITERAL(t):
    r"'.'"
    t.value = t.value.strip("'")
    return t

def t_OPS(t):
    r"\+|\-|\*|\<|\>|\<=|\>=|==|!=|=|\[|\]|\(|\)|{|}|\,|\;"

    #this is just a dictionary to make the function code shorter.
    ops = {'+' : 'PLUS', '-' : 'MINUS', '*' : 'MULTIPLY', '<': 'LESS', '>': 'GREATER',                #OPs
    '>=': 'GTE', '<=': 'LTE', '==': 'EQ', '!=': 'NEQ', '=': 'ASSIGN',                                 #OPs
    '[' : 'LBRACKET', ']' : 'RBRACKET', '{' : 'LBRACE', '}' : 'RBRACE', '(': 'LPAREN', ')': 'RPAREN', #Brackets/Parens
    ',' : 'COMMA', ';' : 'SEMICOLON'}                                                                 #Punctuation
    
    t.type = ops[t.value]
    return t
    
    
def t_STRING_LITERAL(t):
    r'".*"'
    global lexerrs
    #strip off the ""s
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
                    strpieces.append("\\t")
                elif follower == "n":
                    strpieces.append("\\n")
                elif follower == '"':
                    strpieces.append('\\"')
                elif follower == "\\":
                    strpieces.append("\\\\")
                else:
                    #unknown value
                    print "Lexer Error: Unknown escape sequence \\%s in string literal.\n" % value[loc+1]
                    lexerrs += 1
            except:
                print "Lexer Error: String literal ends with an incomplete escape sequence (single '\\').\n"
                lexerrs += 1

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
    r'/\*'
    #scan ahead until we find another */.  If it doesn't exist, then print an error.
    scanahead = data[t.lexpos:]
    location = scanahead.find('*/')
    t.lexer.lineno += len(scanahead[:location].split('\n'))-1
    if location != -1:
        t.lexer.skip(location)
    else:
        print "Lexer Error: Unterminated comment at line %s column %s.\n" % (t.lineno, find_column(data, t))
        global lexerrs
        lexerrs += 1
        #t.lexer.skip(2)
        
    #don't return a value.
    
#this rule is below here because it needs to have lower precedence than t_comments to make sure
#t_comments properly processes comments.  It's probably not necessary to do this.
def t_DIVIDE(t):
    r'/'
    return t
    
    
#Rules that perform a mutation function before returning token
def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)    
    return t
    
# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    #if the first character is a " then we have an unterminated string constant.
    if t.value[0] == '"':
        print "Lexer Error: Unterminated String Constant at Line %s Column %s.\n" % (t.lineno, find_column(data, t))
        #print t
    else:
        print "Lexer Error: Illegal character '%s' at line %s column %s.\n" % (t.value[0], t.lineno, find_column(data, t))
    t.lexer.skip(1)

    global lexerrs
    lexerrs += 1
    
    
    
    
    
    
#------------- ------------- ------------- ------------- 
# end of lexer stuff.
#------------- ------------- ------------- ------------- 
# start of parser stuff.
#------------- ------------- ------------- -------------
    
from tree import Node, makeGraph, getNodes, getTerminals
try:
    from libs import pydot
except:
    print "Unable to import pydot, stuff might crash from here on in."
    
from libs.ply import yacc as yacc
    
global_scope = []
all_local_scopes = {}
local_scope = []
functions = []

#this takes care of the shift-reduce conflict.
precedence = (
    ('right', 'IF'),
    ('right', 'ELSE'),
)




#get a variabble type by looking at scope.
def getType(identifier):
    #check local scope first
    for var in local_scope:
        if var[1] == identifier: #matching name
            return var[0]
    for var in global_scope:
        if var[1] == identifier:#matching name
            return var[0]


def p_start(p):
    'program : declList'
    p[0] = Node("program", p[1:])

def p_declList(p):
    '''declList : decl 
              | decl declList'''
              
    p[0] = Node("declList", p[1:])

def p_decl(p):
    '''decl : varDecl
            | funDecl'''
    if p[1].type == 'varDecl':
        varType = p[1].children[0].children[0].type
        varName = p[1].children[1].type
        global global_scope
        match = False
        for item in global_scope:
            if item[1] == varName: #same identifier
                if item[0] == varType: #same type
                    print "Syntax Error: Redefinition of global %s with type %s near line %s.\n" % \
                          (varName, varType, p.lexer.lineno)
                else:
                    print "Syntax Error: Redefinition of global %s with type %s (originally type %s) near line %s.\n" % \
                          (varName, varType, item[0], p.lexer.lineno)
                global syntaxerrs
                syntaxerrs += 1
                match = True
                    
        if not match:
            if DEBUG:
                print "New global variable %s %s declared near line %s.\n" % (varType, varName, p.lexer.lineno)
            global_scope.append((varType, varName))
            
            
            
    p[0] = Node("decl", p[1:])
    
def p_varDecl(p):
    '''varDecl  : typeSpecifier IDENTIFIER LBRACKET INT_LITERAL RBRACKET SEMICOLON
                | typeSpecifier IDENTIFIER SEMICOLON'''
    p[0] = Node("varDecl", p[1:])
    if len(p) > 4:
        p[0].subtype = "array"
    
def p_typeSpecifier(p):
    '''typeSpecifier : INT
                     | CHAR
                     | VOID
                     | STRING'''
    p[0] = Node("typeSpecifier", p[1:])
    

def p_funDecl(p):
    '''funDecl : typeSpecifier IDENTIFIER LPAREN formalDeclList RPAREN funBody'''
    global local_scope
    #print "Function %s left local scope.  Local scope contains "
    #print local_scope
    all_local_scopes[p[2]] = local_scope
    p[0] = Node("funDecl", p[1:])
    p[0].funcInfo = {'return': getTerminals(p[1])[0], 'numparams':len(local_scope), 'params': local_scope, 'name': p[2]}
    #add function info to tree, and also to the functions.
    #check if the function has already been defined.
    match = False
    for function in functions:
        if function['name'] == p[0].funcInfo['name']:
            global syntaxerrs
            print "Syntax Error: Function %s re-declared near line %s.\n" % (function['name'], p.lexer.lineno)
            syntaxerrs += 1
            match = True
            
    if not match:
        functions.append(p[0].funcInfo)
    
    local_scope = []

def p_formalDeclList(p):
    '''formalDeclList : empty
                      | formalDecl
                      | formalDecl COMMA formalDeclList'''
    p[0] = Node("formalDeclList", p[1:])
    
def p_formalDecl(p):
    '''formalDecl : typeSpecifier IDENTIFIER
                  | typeSpecifier IDENTIFIER LBRACKET RBRACKET'''
    varName = p[2]
    varType = p[1].children[0].type
    for item in global_scope:
        if item[1] == varName:
            if item[0] == varType:
                print "Warning : Shadowing global variable %s near line %s.\n"  % (varName, p.lexer.lineno)
                
    match = False
    for item in local_scope:
        if item[1] == varName: #same identifier
            if item[0] == varType: #same type
                print "Syntax Error: Redefinition of local variable %s with type %s near line %s.\n" % \
                      (varName, varType, p.lexer.lineno)
            else:
                print "Syntax Error: Redefinition of local variable %s with type %s (originally type %s) near line %s.\n" % \
                      (varName, varType, item[0], p.lexer.lineno)
            global syntaxerrs
            syntaxerrs += 1
            match = True
                
    if not match:
        if DEBUG:
            print "New local variable %s %s declared near line %s.\n" % (varType, varName, p.lexer.lineno)
            
        if len(p) > 3:
            local_scope.append((varType, varName, "array"))
        else:
            local_scope.append((varType, varName))
            
    p[0] = Node("formalDecl", p[1:])
    if len(p) > 3:
        p[0].subtype = 'array'
  
def p_funBody(p):
    '''funBody : LBRACE localDeclList statementList RBRACE'''
    #print "function body"
    p[0] = Node("funBody", p[1:])
    
def p_localDeclList(p):
    '''localDeclList : empty
                     | varDecl localDeclList'''
    if len(p) > 2:
        varType = p[1].children[0].children[0].type
        varName = p[1].children[1].type
        global local_scope
        match = False
        for item in global_scope:
            if item[1] == varName:
                if item[0] == varType:
                    print "Warning : Shadowing global variable %s near line %s.\n"  % (varName, p.lexer.lineno)
        for item in local_scope:
            if item[1] == varName: #same identifier
                if item[0] == varType: #same type
                    print "Syntax Error: Redefinition of local variable %s with type %s near line %s.\n" % \
                          (varName, varType, p.lexer.lineno)
                else:
                    print "Syntax Error: Redefinition of local variable %s with type %s (originally type %s) near line %s.\n" % \
                          (varName, varType, item[0], p.lexer.lineno)
                global syntaxerrs
                syntaxerrs += 1
                match = True
                    
        if not match:
            if DEBUG:
                print "New local variable %s %s declared near line %s.\n" % (varType, varName, p.lexer.lineno)
            local_scope.append((varType, varName))
                     
    #print "Local decl list"
    p[0] = Node("localDeclList", p[1:])
    
def p_statementList(p):
    '''statementList : empty
                     | statement statementList'''
    p[0] = Node("statementList", p[1:])
    
def p_statement(p):
    '''statement : compoundStmt
                 | assignStmt
                 | condStmt
                 | loopStmt
                 | returnStmt'''
    p[0] = Node("statement", p[1:])
    
def p_compoundStmt(p):
    '''compoundStmt : LBRACE statementList RBRACE'''
    p[0] = Node("compoundStmt", p[1:])

   
    
        
    
def p_assignStmt(p):
    '''assignStmt : var ASSIGN expression SEMICOLON
                  | expression SEMICOLON'''
                  
    #figure out if it's an assignment of two types...
    if len(p) > 3:
        try:
            var1Name = getTerminals(p[1])[0]
            #try our best to figure out the type of the second item.  just assume the first 'var' we run across is it.
            var2Name = getTerminals(getNodes(p[3], 'var')[0])[0]
            #now do a type lookup.
            var1Type = getType(var1Name)
            var2Type = getType(var2Name)
            if var1Type != var2Type:
                print "Syntax Error: Illegal assignment of variable %s of type %s to variable %s of type %s near line %s.\n" % (var2Name, var2Type, var1Name, var1Type, p.lexer.lineno)
                global syntaxerrs
                syntaxerrs += 1
       
        except:
            pass
    
    p[0] = Node("assignStmt", p[1:])
    
def p_condStmt(p):
    '''condStmt : IF LPAREN expression RPAREN statement
                | ELSE statement'''
    p[0] = Node("condStmt", p[1:])
    
def p_loopStmt(p):
    '''loopStmt : WHILE LPAREN expression RPAREN statement'''
    p[0] = Node("loopStmt", p[1:])
    #p[0] = p[3]


def p_returnStmt(p):
    '''returnStmt : RETURN SEMICOLON
                  | RETURN expression SEMICOLON'''
                  
    p[0] = Node("returnStmt", p[1:])
    
def p_var(p):
    '''var : IDENTIFIER
           | IDENTIFIER LBRACKET addExpr RBRACKET'''
           
    global syntaxerrs
    match = False
    for item in local_scope:
        if item[1] == p[1]:
            match = True
    for item in global_scope:
        if item[1] == p[1]:
            match = True
    if not match:
        print "Syntax Error: Variable \"%s\" is undefined near line %s.\n" %  (p[1], p.lexer.lineno)
        syntaxerrs += 1
    
    #figure out if it's indexed with a variable that turns out not to be an int.
    if len(p) > 2:
        try:
            #first find all variables
            vars = getNodes(p[3], 'var')
            #now check if any of them are not ints.
            for i in vars:
                for terminal in getTerminals(i):
                    if getType(terminal) != None and getType(terminal) != 'int':
                        print "Syntax Error: Illegal Array Index with variable %s of type %s near line %s.\n" % (terminal, getType(terminal),   p.lexer.lineno)
                        syntaxerrs += 1
                        
        except:
            pass
    p[0] = Node("var", p[1:])
    
def p_expression(p):
    '''expression : addExpr
                  | expression relop addExpr'''
    p[0] = Node("expression", p[1:])
    
def p_relop(p):
    '''relop : LTE
             | LESS
             | EQ
             | GREATER
             | GTE
             | NEQ'''
    p[0] = Node("relop", p[1:])
    
def p_addExpr(p):
    '''addExpr  : term
                | addExpr addop term'''
    p[0] = Node("addExpr", p[1:])

def p_addop(p):
    '''addop : PLUS
             | MINUS'''
    p[0] = Node("addop", p[1:])
    
def p_term(p):
    '''term : factor
            | term mulop factor'''

    p[0] = Node("term", p[1:])
    
def p_mulop(p):
    '''mulop : MULTIPLY
             | DIVIDE'''
    p[0] = Node("mulop", p[1:])
    
def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | var
              | funcCallExpr
              | INT_LITERAL
              | CHAR_LITERAL
              | STRING_LITERAL'''
    p[0] = Node("factor", p[1:])

def p_funcCallExpr(p):
    '''funcCallExpr : IDENTIFIER LPAREN argList RPAREN'''
    
    global syntaxerrs
    outstr = ""
    parameters = []
    
    args = getNodes(p[3], ['factor'])
    vals = []
    for arg in args:
        vals.extend(getTerminals(arg))
        
    funcName = p[1]
    #print "function %s called with arguments %s." % (funcName, vals)
    
    #a function is called, let's check that a function exists that matches its signature.
    match = False
    for function in functions:
        if function['name'] == funcName:
            match = True
            #function exists so now let's check if the signature matches.
            if len(vals) > function['numparams']:
                print "Syntax Error: Too many parameters to function %s around line %s.\n" % (funcName, p.lexer.lineno)
                syntaxerrs += 1
            if len(vals) < function['numparams']:
                print "Syntax Error: Too few parameters to function %s around line %s.\n:" % (funcName, p.lexer.lineno)
            else:
                for index, val in enumerate(vals):
                    #if val is a string then it's an identifier name.
                    
                    if type(val) == str:
                        target_type = None
                        #look up the variable in local scope then global scope, and see if it matches.
                        for var in global_scope:
                            if var[1] == val: # matches the name, so it's the right variable, get its type.
                                target_type = var[0]
                        for var in local_scope: #since we do local scope second, automatic shadowing.
                            if var[1] == val:
                                target_type = var[0]
                        if target_type == None:
                            print "Syntax Error: Undeclared identifier %s passed as argument %s to function %s around line %s.\n" % (val, index+1, funcName, p.lexer.lineno)
                            syntaxerrs += 1
                            continue
                    else:
                        target_type = 'int'
                    try:
                        if function['params'][index][0] != target_type:
                            print "Syntax Error: Function %s expects %s (not %s) as parameter %s around line %s.\n" % (funcName, function['params'][index][0], target_type, index+1, p.lexer.lineno)
                            syntaxerrs += 1
                    except IndexError:
                        pass #these are the extra args, no need to have another error.
    
    if not match:
        print "Syntax Error: Undefined Function %s near line %s.\n" % (funcName, p.lexer.lineno)
        syntaxerrs += 1
    p[0] = Node("funcCallExpr", p[1:])
    
def p_argList(p):
    '''argList : empty
               | expression
               | expression COMMA argList'''
    p[0] = Node("argList", p[1:])
    
    
    
    
# Error rule for syntax errors that aren't caught in other parse functions.
def p_error(p):
    if p is None:
        return
    if p.type == 'SEMICOLON':
        print "Syntax Error: terminated expression too soon (extra semicolon) around line %s.\n" % (p.lexer.lineno)
    elif p.type == 'ASSIGN':
        print "Syntax Error: Invalid assignment around line %s.\n" % (p.lexer.lineno)
    elif p.type == 'LBRACE':
        print "Syntax Error: Unmatched left brace near line %s.\n" % (p.lexer.lineno)
    elif p.type == 'LBRACKET':
        print "Syntax Error: Unmatched left bracket near line %s.\n" % (p.lexer.lineno)
    elif p.type == 'IDENTIFIER':
        print "Syntax Error: Undefined identifier %s near line %s.\n" % (p.value, p.lexer.lineno)
    else:
        print "Syntax Error: unable to consume token (%s, '%s'), near line %s.\n" % (p.type, p.value, p.lexer.lineno)
        
    yacc.errok()
    global syntaxerrs
    syntaxerrs += 1

#lets us have empty productions.
def p_empty(p):
    'empty :'
    pass


# Build the lexer
lexer = lex.lex()

# Give the lexer some input
lexer.input(data)

"""
for tok in lexer:
    print tok

"""

print #blank line

# Build the parser
parser = yacc.yacc(debug=True)
#parse it!    
result = parser.parse(data)

print "======================"
print "Global scope: ", global_scope
print "Local Scopes: ", all_local_scopes
print "======================"


#draw the graph...
print "%s lexer errors and %s syntax errors occurred.\n" % (lexerrs, syntaxerrs)
if lexerrs + syntaxerrs > 0:
    print "As some errors occurred, the tree is probably not correct." 
    print "There is some chance that it will still be able to be rendered correctly, but it is not guaranteed."
    
print "drawing graph..."        
try:
    graph = pydot.Dot(graph_type='digraph')  
    makeGraph(graph, result)
    graph.set_graphviz_executables(paths={'dot': dotpath})
    graph.write_svg(graph_out, prog='dot')
    print "graph drawn."
    
except:
    print "Unable to draw graph.  Perhaps you don't have Graphviz installed, or your dotpath is set wrong at the top of main.py?"
