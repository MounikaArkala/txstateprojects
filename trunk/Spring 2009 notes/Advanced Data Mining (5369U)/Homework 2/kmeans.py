#!/usr/bin/python
#Virpobe Paireepinart
#Advanced Data Mining
#Spring 2010 Texas State University


import random, math
DEBUG = False # set to True to get debug messages.

def distance(pt1, pt2): #euclidean distance between 2 points.  not very generalized.
    return math.sqrt((pt1[1] - pt2[1])**2 + (pt1[0] - pt2[0])**2)
    
def centroid(points): # calculates the centroid of a list of points.
    x = sum([i[0] for i in points])/float(len(points))
    y = sum([i[1] for i in points])/float(len(points))
    return (x,y)


def kmeans(k, points): # calculate the k 'kmeans' clusters of a list of points.
    if DEBUG:
        print "Running k-means (k = %s)." % k
    
    clusters = [[] for i in range(k)]
    centroids = [-1 for i in range(k)]
    clusterids = {}
    
    for i in range(k):
        try:
            temp = points.pop(random.randrange(len(points)))
            clusters[i].append(temp)
            clusterids[temp] = i
        except ValueError:
            return clusters
    centroids = [centroid(i) for i in clusters]
    #place the rest of the "k" items into clusters based on centroid.
    for point in points:
        mindist = distance(point, centroids[0])
        mincentroid = 0
        for index, c in enumerate(centroids):
            if distance(point, c) < mindist:
                mincentroid = index
        clusters[mincentroid].append(point)
        clusterids[point] = mincentroid
        #recalculate centroids
        centroids = [centroid(i) for i in clusters]
    if DEBUG:
        print "\nInitial Clusters:"
        print "------"
        for cluster in clusters:
            print cluster
        print "------\n"
    #now all are clustered, we can begin the reclustering step.
    #basically we go through every sample, and check which cluster it should be in.
    #if it is not in the correct cluster, we add it to the correct cluster
    #and recalculate the centroids.
    
    time_to_exit = False
    while not time_to_exit:
        if DEBUG:
            print "\nStarting recluster step..."
        #set it to true, that way we only run thru the list once unless a move is made.
        time_to_exit = True
        
        
        for point in clusterids.keys():
            mindist = distance(point, centroids[clusterids[point]]) # dist between point and its current cluster's centroid.
            mincentroid = clusterids[point]
            movepoint = False
            for index, c in enumerate(centroids):
                if distance(point, c) < mindist:
                    mincentroid = index
                    movepoint = True
            if movepoint:
                if DEBUG:
                    print "Moving point ", point
                #move the point to the new cluster from its old cluster.
                #also it's no longer time to finish the loop since we have made a change.
                time_to_exit = False
                i = clusterids[point]
                clusters[i].pop(clusters[i].index(point))
                clusters[mincentroid].append(point)
                clusterids[point] = mincentroid
                #recalculate centroids
                centroids = [centroid(i) for i in clusters]
            else:
                if DEBUG:
                    print "Not moving point ", point
        if time_to_exit:
            if DEBUG:
                print "No points were moved in this step."
    if DEBUG:
        print "\n\nCentroids:"
        print "-----"
        print centroids
        print "-----"
    return clusters
            
import sys
if len(sys.argv) < 3:
    print "usage: kmeans k infile"
    raise SystemExit
filename = sys.argv[2]
tuples = [tuple(map(int, i.strip().split())) for i in open(filename).readlines()]
k = int(sys.argv[1])
if DEBUG:
    print "\n\nStarting with initial input data: "
    print "------"
    print tuples
    print "------\n"
    
print "About to begin clustering. k = %s." % k
clusters = kmeans(k, tuples)
if DEBUG:
    print "\n\n"
    print "Final clusters: "
    print "-----"
    for cluster in clusters:
        print cluster
    print "-----"
    print "\n\n"
print "writing clusters to output.txt ...."
outfile = open("output.txt", "w")
for i, cluster in enumerate(clusters):
    for point in cluster:
        outfile.write("%i\t%i\t%i\n" % (point[0], point[1], i+1))
outfile.close()

print "clusters written to output.txt."