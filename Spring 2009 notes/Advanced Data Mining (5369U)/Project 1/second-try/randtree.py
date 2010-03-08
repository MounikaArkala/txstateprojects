
import random, orange

class TreeNode(object):
    def __init__(self, splitvar, index, datapoint, usedattrs):
        #subtrees are indexed by the splitvar, and they are by definition None
        #unless some data is contained in them.
        self.splitvar = splitvar
        self.subtrees = {}
        self.index = index
        for i in splitvar.values:
            self.subtrees[i] = None
            
        self.subtrees[datapoint[index].value] = [datapoint]
        #self.subtrees[datapoint[splitvar.values]] = datapoint#self.subtrees[data[0]] = data[1]
        self.usedattrs = usedattrs
        
    def add(self, data):
        #attempt to add a new node to the tree, if the location can't be found, split and add a new TreeNode.
        
        existingval = self.subtrees[data[self.index].value]
        if existingval == None:
            #print "was added without making any new subtrees."
            self.subtrees[data[self.index].value] = [data]
            
        #if it's a tree, call add() on it.
        elif type(existingval) == type(self):
            existingval.add(data)
        #otherwise we just add it to the base case.
        else:
            #one already exists.
            #check if class matches.
            if existingval[0][-1] == data[-1]: #assume class is last variable.
                #they're the same class so we can group them together for now.
                existingval.append(data)
            else:
                # we need to split on another variable and then move all of the current subtree items into the new subtree-tree.
                #first let's choose a new splitting variable.
                attrs = data.domain
                #print "attrs:", attrs
                targets = []
                for item in attrs:
                    if item not in self.usedattrs:
                        targets.append(item)
                        
                possible_attrs = len(targets)
                chosen = random.randrange(possible_attrs)
                x = self.usedattrs[:]
                x.append(targets[chosen])
                temp = [i for i in data.domain]
                newnode = TreeNode(targets[chosen], temp.index(targets[chosen]), data, x)
                for item in existingval:
                    newnode.add(item)
                existingval = []
                self.subtrees[data[self.index].value] = newnode
                #move all data to new node.
                #print data, " could not be added."
                
                
    def __repr__(self):
        temp = "Subtrees: " + str(self.subtrees) + "\n"
        return temp + "usedattrs: " + str(self.usedattrs)
        
def makeTree(data):
    # we assume class var is the last item.
    #figure out all possible values for each item.
    
    possible_attrs = len(data[0].domain)-1
    chosen = random.randrange(possible_attrs)
    head = TreeNode(data[0].domain[chosen], chosen, data[0], [data[0].domain[chosen], data[0].domain[len(data[0].domain)-1]])
    for datum in data:
        head.add(datum)
    return head
    
def height(startNode, current=0, maxheight=0):
    if current > maxheight:
        maxheight = current
    terminal = False
    for tree in startNode.subtrees.values():
        if type(tree) == type(startNode):
            maxheight = height(tree, current+1, maxheight=maxheight)
        elif tree != None:
            #there's a terminal node here.
            terminal = True
    if terminal:
        current += 1
    if current > maxheight:
        maxheight = current
    return maxheight
    
    
def getClass(startNode, targetData):
    #print "startNode: ", startNode
    #basically we branch down each path following our item's split class, and when we end up at a terminal node, we return its class.
    #we might end up at a None and then we return None and the calling getClass must return its class??? I guess?
    #if type(startNode) == list:
    #    target_class = startNode[-1]
    #else:
    #print "Data", targetData
    split_tree = startNode.subtrees[targetData[startNode.index].value]
    if split_tree == None:
        #were unable to classify (that means it's a negative)
        return None
        
    if type(split_tree) == list:
        #found the pool of matches that we're supposed to be in.
        firstitem = split_tree[0][-1]
        for item in split_tree:
            if item[-1] != firstitem:
                print "spurious item", firstitem, "doesn't match", item
        #print split_tree[0][-1]
        target_class = split_tree[0][-1]
    else:
        #we haven't reached a dead end yet.
        #recurse.
        target_class = getClass(split_tree, targetData)
        #if we don't end up in a pool then we will return a None value for target_class.

   # print "returning from getClass"
    return target_class