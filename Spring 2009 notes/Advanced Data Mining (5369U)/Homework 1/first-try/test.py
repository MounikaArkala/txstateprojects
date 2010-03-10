from dtree import *
from c45 import *
import sys


def get_file():
    """
    Tries to extract a filename from the command line.  If none is present, it
    prompts the user for a filename and tries to open the file.  If the file 
    exists, it returns it, otherwise it prints an error message and ends
    execution.
    """
    # Get the name of the data file and load it into 
    if len(sys.argv) < 2:
        # Ask the user for the name of the file
        filename = raw_input("Filename: ").strip()
    else:
        #fixed weird code here, Luke P.
        filename = sys.argv[1]

    try:
        fin = open(filename)
    except IOError:
        print "Error: The file '%s' was not found on this system." % filename
        sys.exit(0)

    return fin

def run_test(fin):
    """
    This function creates a list of exmaples data (used to learn the d-tree)
    and a list of samples (for classification by the d-tree) from the
    designated file.  It then creates the d-tree and uses it to classify the
    samples.  It prints the classification of each record in the samples list
    and returns the d-tree.
    """
    # Create a list of all the lines in the data file
    lines = [line.strip() for line in fin.readlines()]

    # Remove the attributes from the list of lines and create a list of
    # the attributes.
    
    #fixed weird code here, Luke P.
    attributes = [attr.strip() for attr in lines.pop(0).split(",")]
    target_attr = attributes[-1]

    # Create a list of the data in the data file
    #fixed weird code here, Luke P.
    data = [dict(zip(attributes,
                             [datum.strip() for datum in line.split(",")])) for line in lines]
        
    # Copy the data list into the examples list for testing
    examples = data[:]
    
    # Create the decision tree
    tree = create_decision_tree(data, attributes, target_attr, gain)
    #randtree = create_decision_tree(data, attributes, target_attr, 'RANDOM')

    # Classify the records in the examples list
    classification = classify(tree, examples)

    # Print out the classification for each record
    for item in classification:
        print item

    return tree

def print_tree(tree, str):
    """
    This function recursively crawls through the d-tree and prints it out in a
    more readable format than a straight print of the Python dict object.  
    """
    if type(tree) == dict:
        print "%s%s" % (str, tree.keys()[0])
        for item in tree.values()[0].keys():
            print "%s\t%s" % (str, item)
            print_tree(tree.values()[0][item], str + "\t")
    else:
        print "%s\t->\t%s" % (str, tree)


if __name__ == "__main__":

    #increase recursion limit so we can work with bigger files.
    sys.setrecursionlimit(10000)
    x = sys.stdout
    sys.stdout = open('output.txt', 'w')
    fin = get_file()
    print
    print "------------------------"
    print "--   Classification   --"
    print "------------------------"
    print  
    tree = run_test(fin)
    print 
    print "------------------------"
    print "--   Decision Tree    --"
    print "------------------------"
    print
    print_tree(tree, "")
    sys.stdout.close()
    sys.stdout = x
    fin.close()
