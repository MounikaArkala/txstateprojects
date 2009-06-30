

values = [0,1,2,3,4,5,6,7]

def shuffle():
    temp = values[4]
    values[4] = values[2]
    values[2] = values[1]
    values[1] = temp
    temp = values[3]
    values[3] = values[5]
    values[5] = values[6]
    values[6] = temp
    print values
    
def exchange():
    for i in range(0,8,2):
        temp = values[i]
        values[i] = values[i+1]
        values[i+1] = temp
    
    print values
