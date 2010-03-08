import orange
data = orange.ExampleTable("car")
classifier = orange.BayesLearner(data) # compute classification accuracy

def printTabDelimContingency(c):
    print c


orange.setoutput(orange.BayesClassifier, "tab", printTabDelimContingency) 
print classifier.dump('tab')
correct = 0.0
for ex in data: 
    if classifier(ex) == ex.getclass():
        correct += 1
        #print "Classification accuracy:", correct/len(data) 