import sys, random
import orange, orngStat
from orngStat import *
from orngTest import *
import randtree, c45tree

#if they passed a command line arg let's use it as an output file name.
if len(sys.argv) > 1:
    output = sys.argv[1]
    target = open(output, 'w')
    print "Running... output redirected to %s" % output
    oldout = sys.stdout
    sys.stdout = target
else:
    print "Running... output will be in console."
 
#process every file in directory 'datasets' that has the extension '.tab'
datadir = 'datasets'
for i in [j for j in os.listdir(datadir) if os.path.splitext(j)[-1] == ".tab"]:
    data = orange.ExampleTable(os.path.join(datadir, i))
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
    
    #Cross-validate random tree 3 times, keep track of total accuracy and height for printing later.
    totalavg_accuracy = 0
    totalavg_height = 0
    for run in range(3):
        print "Run %s of Random Tree..." % (run+1)
        
        
        #divide up data for 10-fold cross-validation - keep track of accuracy / height
        #for each of 10 runs and avg them at the end.
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
            
            #make our tree
            head = randtree.makeTree(trainingdata)
            classification_accuracy = 0
            for ex in testdata:
                #if it's accurately classified add one, otherwise don't do anything.
                if ex[-1] == randtree.getClass(head, ex):
                    classification_accuracy += 1
                    
            avg_accuracy += classification_accuracy/float(len(testdata))
            
            height = randtree.height(head)
            avg_height += float(height)
        
        #fix our averages and print everything out.
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

    #now we just do the c4.5 stuff, it's easy because we don't have to 
    #reimplement 10-fold cross validation since their builtin function works with it.
    print "Run 1 of C45 Tree..."
    #setup the c4.5 tree.
    c45 = orange.C45Learner()
    c45.name = "C4.5"
    learners = [c45]
    #learn the tree on the data and store the classifiers in results.classifiers so we can check their height later.
    results = crossValidation(learners, data, folds=10, strat=True, storeclassifiers=True)

    avg_height = 0
    for classifierset in results.classifiers:
        height = c45tree.height(classifierset[0])
        avg_height += float(height)
        
    avg_height /= 10
    print "Accuracy:", CA(results)[0]
    print "Height:", avg_height
            
    print "\n\n\n\n\n"

#switch stdout back to console if it's at the file right now.
if len(sys.argv) > 1:
    target.close()
    sys.stdout = oldout
print "Done..."