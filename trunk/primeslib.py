def all_perms(str):
    #~~ PUBLIC DOMAIN FUNCTION FROM MICHAEL DAVIES
    if len(str) <=1:
        yield str
    else:
        for perm in all_perms(str[1:]):
            for i in range(len(perm)+1):
                yield perm[:i] + str[0:1] + perm[i:]

                
def prime(notes, degree):
    """ notes is int array, degree is the prime degree (0, 1, 2, etc.)"""
    return [(i + degree) % 12 for i in notes]

def inversion(notes, degree):
    """ notes is int array, degree is the prime degree (0, 1, 2, etc.)"""
    newnotes = []
    newnotes.append(notes[0])
    """ invert around the line of symmetry that originates at notes[0]"""
    symmetry = notes[0] % 6
    #algorithm goes thustly:
    #say our inversion axis is 4.  any inversion axis is going to be from 0-5
    #because if it's 6 it's the same as 0, 7 is the same as 1, etc.
    #so say our axis is 3.  then anything greater than 3 and less than
    #3 + 6 will be swapped to the other side, anything less than 3 and greater
    # than 3 + 6 will be swapped to the other side, and everything else will
    #stay the same.
    #inverting something around an axis such as 3:
    # 3 -> 3
    # 4 -> 2
    # 5 -> 1
    # we just do
    # original -= (original - 3) * 2
    for note in notes[1:]:
        if note > symmetry and note < symmetry + 6:
            newnotes.append((note - (note - symmetry) * 2) % 12)
        elif note < symmetry or note > symmetry + 6:
            newnotes.append((note + (symmetry - note) * 2) % 12)
        else:
            newnotes.append(note)
    return [(i + degree) % 12 for i in newnotes]

def retrograde(notes, degree):
    """ notes is int array, degree is the prime degree (0, 1, 2, etc.)"""
    notes = prime(notes, degree)
    notes.reverse()
    return notes

def retrograde_inversion(notes, degree):
    """ notes is int array, degree is the prime degree (0, 1, 2, etc.)"""
    #make sure you don't use degree twice! only need to transpose once!
    return retrograde(inversion(notes, degree), 0)



def find_in_list(alist, sublist, wraparound=False):
    """ generic function that detects if sublist occurs in alist anywhere. wraparound makes alist circular."""
    first_index = alist.index(sublist[0])
    for item in sublist[1:]:
        if alist.index(item) == first_index + 1:
            first_index += 1
        else:
            return -1
    return alist.index(sublist[0])

def detect(notes, search):
    # search through all possible inversions, retrogrades, primes and retrograde inversions for the series.
    functs = [("Prime", prime), ("Retrograde", retrograde), ("Inversion", inversion),
	          ("Retrograde Inversion", retrograde_inversion)]
    matches = []
    for name, func in functs:
        for x in range(12):
            temp = func(notes, x)
            result = find_in_list(temp, search)
            if result >= 0:
                matches.append((name, x, result, temp))
    return matches




