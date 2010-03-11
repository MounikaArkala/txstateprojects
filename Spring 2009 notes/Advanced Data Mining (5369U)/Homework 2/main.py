import random, math
DEBUG = False
#TODO: make clustering have to have at least 1 item?  not sure if this is valid or not, sometimes my clusters do not have any items in them.
def distance(pt1, pt2):
    return math.sqrt((pt1[1] - pt2[1])**2 + (pt1[0] - pt2[0])**2)
    
def medoid(points):
    x = sum([i[0] for i in points])/float(len(points))
    y = sum([i[1] for i in points])/float(len(points))
    return (x,y)


def kmeans(k, tuple, means=None):
    if DEBUG:
        print "Running k-means (k = %s)." % k
    if not means:
        means = tuple[:]
        temp = []
        for i in range(k):
            temp.append(means.pop(random.randrange(0, len(means)) ))
        means = temp
    
    clusters = [[] for i in range(k)]
    if DEBUG:
        print "means: ", means
    
    #assign all items in tuple to a cluster, calculate each cluster's medoid.
    if DEBUG:
        print "performing clustering..."
        
    for point in tuple:
        mindist = distance(point, means[0])
        cluster = 0
        for c, mean in enumerate(means[1:]):
            if distance(point, mean) < mindist:
                cluster = c + 1
        clusters[cluster].append(point)
        
    if DEBUG:
        print "Clusters: "
        print clusters
        print "recalculating means..."
    newmeans = []
    for cluster in clusters:
        if len(cluster) == 0:
            newmeans.append((-1,-1))
        else:
            newmeans.append(medoid(cluster))#HACK: TODO: FIX
    if DEBUG:
        print newmeans
    
    #if medoids are same as means then break, done.
    #otherwise, recurse.
    for i in range(len(means)):
        if means[i] != newmeans[i]:
            if DEBUG:
                print "one or more means changed, re-clustering:"
            clusters = kmeans(k, tuple, means=newmeans)
    if DEBUG:
        print "means did not change, stopping recursion."
    return clusters
    
tuples = [tuple(map(int, i.strip().split())) for i in open('input.txt').readlines()]
clusters = kmeans(6, tuples)
print "\n\n\n"
print "Clusters: ", clusters
print "writing clusters to output.txt ...."
outfile = open("output.txt", "w")
for i, cluster in enumerate(clusters):
    for point in cluster:
        outfile.write("%i %i %i\n" % (point[0], point[1], i+1))
outfile.close()

print "clusters written to output.txt."