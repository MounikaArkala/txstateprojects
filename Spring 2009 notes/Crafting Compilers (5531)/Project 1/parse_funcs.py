from config import toks, debug
#TODO: make real Exception objects rather than just printing the error to stdout.
#also: when an exception occurs, catch it in the scanner, that way all exceptions will be reported with correct column + line numbers
# (we can even fancy print the line and put an arrow at the column that the error occured on).

def tokenize(value): # used for operators, punctuation, parens/brackets, and keywords.
    if debug:
        if toks[value] > 254 and toks[value] < 263:
            return "%s [Keyword]: %s" % (str(toks[value]), value)
        else:
            return "%s [Token]: %s" % (str(toks[value]), value)
    return str(toks[value])
    
def sliteral(value): #used for string literals
    #first we need to take away the outer quotes.
    value = value[1:-1]
    
    #now we need to make sure this is a valid string literal.value = 
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
    if debug:
        return "%s [String]: %s" % ( str(toks["STRCONST"]), value)
    return str(toks["STRCONST"]) + " " + value
    
def iliteral(value): #used for integer literals
    if debug:
        return "%s [Integer]: %s" % (str(toks["INTCONST"]), value)
    return str(toks["INTCONST"]) + " " + value
    
def cliteral(value): #used for character literals
    if debug:
        return "%s [Char]: %s (%s)" % (str(toks["CHARCONST"]), str(ord(value.strip("'"))), value)

    return str(toks["CHARCONST"]) + " " + str(ord(value.strip("'")))
    

def identifier(value): # used for identifiers
    if debug:
        return "%s [Identifier]: %s" % (str(toks["ID"]), value)
    return str(toks["ID"]) + " " + value
    
def nothing(value):
    return ""




