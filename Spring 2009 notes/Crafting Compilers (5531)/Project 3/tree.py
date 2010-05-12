# ------------------------------------------------------------
# Trees.py by Luke Paireepinart, Texas State University, Spring 2010
# 
# This is a few custom classes/functions I wrote,
# for easy creation and rendering of AST's.
# ------------------------------------------------------------


#This is a generic Node class.  The tree is made of Node's.
#a tree with no self.children is by definition a leaf node.
#all other nodes are nonterminal nodes.
#in the AST, all nonterminal nodes represent nonterminals in the grammar,
#and all terminal nodes represent terminals.  Nice, right? :)
class Node(object):
    def __init__(self,nodetype,*kwargs):
        self.type = nodetype
        self.children = []
        if len(kwargs) > 0:
            kwargs = kwargs[0]
        for item in kwargs:
            #if it's not already a node, add it as a leaf node.  a leaf node is just a node w/ no children (default).
            if type(item) != type(self):
                self.children.append(Node(item))
            #otherwise add it directly.
            else:
                self.children.append(item)
                
from libs import pydot

#This function takes a graph and a root node as input.
#traverses the tree and recursively adds items to the graph
#(as subtrees of parent, if defined, otherwise they become parent node.)
#it's up to the caller to render the graph to a file.
#the 'val' is used to create a unique identifier.  Otherwise
#the default is to use the label and the value of a node to be the same,
#so if you have 2 different nodes as ';' for example,
#then the graph will collapse them.  We use 'val' to have unique
#id's for every node in the graph so that the nodes won't collapse.
def makeGraph(graph, tree, parent=None, val=0):
    if tree == None:
        return val
    
    #this is to change the name from "" to "empty" for empty productions.
    if tree.type == None:
        tree.type = "empty"
    
    node = pydot.Node(name=str(val), label=str(tree.type))
    graph.add_node(node)
    val += 1
    
    if parent != None:
        graph.add_edge(pydot.Edge(parent, node))
        
    #recurse so subtrees will append themselves to graph.
    for subtree in tree.children:
        val = makeGraph(graph, subtree, node, val)
    
    return val
    

    #get all nodes that match a certain name from the tree.
def getNodes(tree, nodenames, prevnodes=None):
    #print "searching ", tree, "for ", nodenames
    #print "tree is: ", tree.type
    if prevnodes == None:
        prevnodes = []
    if tree == None:
        return prevnodes
        
    for child in tree.children:
        prevnodes = getNodes(child, nodenames, prevnodes)
        
    if tree.type in nodenames:
        prevnodes.append(tree)
        
    return prevnodes
    

def getTerminals(tree, terminals=None):
    if terminals == None:
        terminals = []
        
    if tree == None:
        return terminals
        
        
    if len(tree.children) == 0:
        terminals.append(tree.type)
    else:
        for child in tree.children:
            terminals = getTerminals(child, terminals)
    
    return terminals
    
        
    
    