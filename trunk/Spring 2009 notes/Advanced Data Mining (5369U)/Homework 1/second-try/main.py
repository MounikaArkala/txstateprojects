import sys, random

import orange, orngStat
from orngStat import *
from orngTest import *


    
import randtree, c45tree

target = open('output.txt', 'w')
print "Running... output redirected to output.txt"
oldout = sys.stdout
sys.stdout = target
for i in [j for j in os.listdir('datasets') if os.path.splitext(j)[-1] == ".tab"]:
    data = orange.ExampleTable(os.path.join('datasets', i))
    print "===================================================================="
    print "Dataset:", " ".join(os.path.splitext(i)[:-1])
    print "there are %s data." % len(data)
    print "each example includes %s attributes:" % len(data[0])
    print
    names = [i.name for i in data.domain]
    print ", ".join(names)
    print
    print "The class is:", names[-1]
    print "===================================================================="
    #Cross-validate random tree 3 times.
    totalavg_accuracy = 0
    totalavg_height = 0
    for run in range(3):
        print "Run %s of Random Tree..." % (run+1)
        
        
        #divide up data for 10-fold cross-validation
        """
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
        """ 
        avg_accuracy = 0
        avg_height = 0
        grouplen = len(data)*1.0 / 10
        for i in range(10):
            trainingdata = []
            testdata = []
            for e,item in enumerate(data):
                #basically if we're in range of testarea put items in test data set
                #otherwise put them in training data set.
                if i*grouplen < e < i*grouplen+grouplen:
                    testdata.append(item)
                else:
                    trainingdata.append(item)
            
            head = randtree.makeTree(trainingdata)
            classification_accuracy = 0
            for ex in testdata:
                if ex[-1] == randtree.getClass(head, ex):
                    classification_accuracy += 1
                    
            avg_accuracy += classification_accuracy/float(len(testdata))
            
            height = randtree.height(head)
            avg_height += float(height)
            
        avg_accuracy /= 10
        avg_height /= 10
        print "Accuracy:", avg_accuracy
        print "Height:", avg_height
        totalavg_accuracy += avg_accuracy
        totalavg_height += avg_height
        print "\n"
        
    totalavg_accuracy /= 3
    totalavg_height /= 3
    print "Total Accuracy Avg (over all 3 runs): ", totalavg_accuracy
    print "Total Height  Avg  (over all 3 runs): ", totalavg_height
    print
    print "Run 1 of C45 Tree..."     
    c45 = orange.C45Learner()
    c45.name = "C4.5"
    
    learners = [c45]

    results = crossValidation(learners, data, folds=10, strat=True, storeclassifiers=True)

    avg_height = 0
    for classifierset in results.classifiers:

        height = c45tree.height(classifierset[0])
        avg_height += float(height)
        #print dir(classifierset[1])
    #print results.classifiers
    avg_height /= 10
    print "Accuracy:", CA(results)[0]
    print "Height:", avg_height
            
    print "\n\n\n\n\n"

target.close()
sys.stdout = oldout
print "Done..."