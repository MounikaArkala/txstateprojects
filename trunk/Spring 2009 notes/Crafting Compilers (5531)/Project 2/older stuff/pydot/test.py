
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
            
                

         

AST = Node("parent", Node('Child1', 'leaf1'), Node('Child2', Node('Child3', 'leaf3')), 'parentleaf')
import pydot

# this time, in graph_type we specify we want a DIrected GRAPH
graph = pydot.Dot(graph_type='digraph')

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
    
    
makeGraph(graph, AST)
graph.set_graphviz_executables(paths={'dot': r'C:\Program Files (x86)\Graphviz2.26.3\bin\dot.exe'})
graph.write_png('graph_dot.png', prog='dot')

