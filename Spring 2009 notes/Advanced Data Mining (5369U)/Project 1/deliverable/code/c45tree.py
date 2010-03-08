import orange
    
    
    
#printer for c45 Trees. set verbose to True to see the tree in the output.  Otherwise
# returns height.  I don't actually use printTree in final product but I used it in testing.
#helper func for printTree.
def printTree0(node, classvar, lev, maxlevel=0, verbose=False):
    var = node.tested
    if lev > maxlevel: maxlevel = lev
    if node.nodeType == 0:
        if verbose:
            print "%s (%.1f)" % (classvar.values[int(node.leaf)], node.items),

    elif node.nodeType == 1:
        for i, val in enumerate(var.values):
            if verbose:
                print ("\n"+"|    "*lev + "%s = %s:") % (var.name, val),
            maxlevel = printTree0(node.branch[i], classvar, lev+1, maxlevel=maxlevel, verbose=verbose)

    elif node.nodeType == 2:
        if verbose:
            print ("\n"+"|    "*lev + "%s <= %.1f:") % (var.name, node.cut),
        maxlevel = printTree0(node.branch[0], classvar, lev+1, maxlevel=maxlevel)
        if verbose:
            print ("\n"+"|    "*lev + "%s > %.1f:") % (var.name, node.cut),
        maxlevel = printTree0(node.branch[1], classvar, lev+1, maxlevel=maxlevel, verbose=verbose)

    elif node.nodeType == 3:
        for i, branch in enumerate(node.branch):
            inset = filter(lambda a:a[1]==i, enumerate(node.mapping))
            inset = [var.values[j[0]] for j in inset]
            if verbose:
                if len(inset)==1:
                    print ("\n"+"|    "*lev + "%s = %s:") % (var.name, inset[0]),
                else:
                    print ("\n"+"|    "*lev + "%s in {%s}:") % (var.name, reduce(lambda x,y:x+", "+y, inset)),
            maxlevel = printTree0(branch, classvar, lev+1, maxlevel=maxlevel, verbose=verbose)

    return maxlevel
    
def printTree(tree):
    maxlevel = printTree0(tree.tree, tree.classVar, 0)
    return maxlevel
    
    
    
    
#Height Calculation functions
#helper func for height. 
def heighthelper(node, classvar, lev, maxlevel=0):
    verbose = False
    var = node.tested
    if lev > maxlevel:
        maxlevel = lev

    if node.nodeType == 1:
        for i, val in enumerate(var.values):
            maxlevel = heighthelper(node.branch[i], classvar, lev+1, maxlevel=maxlevel)

    elif node.nodeType == 2:
        maxlevel = heighthelper(node.branch[1], classvar, lev+1, maxlevel=maxlevel)

    elif node.nodeType == 3:
        for i, branch in enumerate(node.branch):
            inset = filter(lambda a:a[1]==i, enumerate(node.mapping))
            inset = [var.values[j[0]] for j in inset]
            maxlevel = heighthelper(branch, classvar, lev+1, maxlevel=maxlevel)

    return maxlevel
       
def height(tree):
    maxlevel = heighthelper(tree.tree, tree.classVar, 0)
    return maxlevel
    
    
