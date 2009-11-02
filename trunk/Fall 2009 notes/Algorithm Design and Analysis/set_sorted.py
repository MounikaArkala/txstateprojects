
def union(A, B):
    result = []
    a = 0
    b = 0
    while a < len(A) and b < len(B):
        if result:
            if a < len(A) and result[-1] == A[a]:
                a += 1
                continue
            if b < len(B) and result[-1] == B[b]:
                b += 1
                continue
            
        if a >= len(A):
            #A is out of items, just insert B.
            result.append(B[b])
        elif b >= len(B):
            result.append(A[a])
            
        elif A[a] < B[b]:
            #A[a] is lower.
            result.append(A[a])
            
        else:
            result.append(B[b])
    return result

import time, random
for x in range(20,40):
    
    A = [random.choice(range(100)) for i in range(2 ** x)]
    A.sort()
    B = [random.choice(range(100)) for i in range(2 ** x)]
    B.sort()
    print "starting!"
    starttime = time.time()
    #print union(A, B)
    runtime = time.time() - starttime
    print "took", runtime, "to run."