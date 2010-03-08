  
    
"""
#function to print regular Trees.  set verbose to True in the function call to see the tree output.
#otherwise you just get the height.
def printTree1(node, level, maxlevel=0, verbose=False):
    if level >= maxlevel:
        maxlevel = level
    if not node:
        #print " "*level + "<null node>"
        return maxlevel
        
    if node.branchSelector:
        nodeDesc = node.branchSelector.classVar.name
        nodeCont = node.distribution
        if verbose:
            print "\n" + " "*level + "%s (%s)" % (nodeDesc, nodeCont),
        for i in range(len(node.branches)):
            if verbose:
                print "\n" + " "*level + ": %s" % node.branchDescriptions[i],
            maxlevel = max(maxlevel, printTree1(node.branches[i], level+1, maxlevel=maxlevel, verbose=verbose))
    else: 
        nodeCont = node.distribution
        majorClass = node.nodeClassifier.defaultValue
        if verbose:
            print "--> %s (%s) " % (majorClass, nodeCont), 
        
    if level >= maxlevel:
        maxlevel = level
    return maxlevel
    
def myLearner(examples, weightID = 0):
    #print dir(examples[0])
    #print ""
    #print ""
    rc = orange.RandomClassifier()
    rc.classVar = data.domain.classVar
    randitems = examples[0].domain
    
    temp = [0] * len(randitems)
    for x in range(1000):
        temp[random.randrange(len(temp))] += 1/1000.
        
    #if x >= val:
    #    temp.append(val)
    #else:
    #    temp.append(x)
        
    rc.probabilities = temp
    rc.defaultValue = data.domain.classVar
    return rc
    
def depth(tree):
     if not tree.branches:
         return 1
     else:
         return max([depth(branch) for branch in tree.branches]) + 1



treeLearner = orange.TreeLearner()
treeLearner.nodeLearner = myLearner
print
print
print "Data Size: ", len(data)

for run in range(3):
    print "Run %s of Random Tree..." % (run+1)
    #divide up data for 10-fold cross-validation
    numgroups = len(data)*1.0 / 10
    groups = []
    for i in range(10):
        temp = []
        #because Orange doesn't allow slices
        for y in range(int(numgroups)):
            temp.append(data[int(i*numgroups+y)])
        groups.append(temp)
    #grab any remaining values and put them in the last item.
    for z in range(int(10*numgroups), len(data)):
        groups[-1].append(data[z])
        
    print [len(i) for i in groups]
    avg_accuracy = 0
    avg_height = 0
    for i in range(10):
        testdata = groups[i]
        trainingdata = []
        for z in range(i):
            trainingdata.extend(groups[i])
        for z in range(i+1, 10):
            trainingdata.extend(groups[i])
        #print len(trainingdata)
        
        tree = treeLearner(trainingdata)
        height = depth(tree.tree)#printTree1(tree.tree, 0)
        classification_accuracy = 0
        for ex in testdata:   
            #print ex[-1], tree(ex)
            if ex[-1] == tree(ex):
                classification_accuracy += 1
        avg_accuracy += classification_accuracy/float(len(testdata))
        avg_height += float(height+1)
        
    avg_accuracy /= 10
    avg_height /= 10
    print "Accuracy:", avg_accuracy
    print "Height:", avg_height
        
"""