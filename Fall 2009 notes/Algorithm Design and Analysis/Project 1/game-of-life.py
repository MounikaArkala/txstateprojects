"""
Name: Virpobe Luke Paireepinart
Date: 9/30/09
Project Number: 1
ALG CS5329
Instructor: Komogortsev, TSU
"""
import copy, random, time

def print_board(board):
    #outputs a board to the screen so the user can see the current configuration.
    #assumes board is inflated on all sides w/ a hedge.
    print  "_" * ((len(board[0]) - 2) * 2 + 1)
    out = ""
    for row in board[1:-1]:
        temp = ""
        for col in row[1:-1]:
            if col <= 0:
                temp += "|_"
            else:
                temp += "|@"
        temp += "|\n"
        out += temp
    
    print out
        
        
def neighbors(board, row, col):
    #calculates the number of neighbors a cell contains.
    #assumes board is inflated w/ a hedge but indexes aren't already adjusted for hedge.
    row += 1
    col += 1
    return sum([sum(board[row-i][col-1:col+2]) for i in range(-1,2)]) - board[row][col]

    
def gol2(board, width, height, iterations, debug=False, output=False):
    #the 2nd gol simulation implementation
    temp = copy.deepcopy(board)
    board = temp
    num_neighbors = []
    maylive = []
    maydie = []
    newlive = []
    newdie = []
    
    #initialize everything.
    for rowindex,row in enumerate(board[1:-1]):
        temp = []
        for colindex,col in enumerate(row[1:-1]):
            num = neighbors(board, rowindex, colindex)
            temp.append(num)
            if col: #it's alive
                if not 2 <= num <= 3: #it may die
                    maydie.append((rowindex,colindex))
            else:
                if num == 3: #it may live
                    maylive.append((rowindex,colindex))
                        
        num_neighbors.append(temp)

    if output:
        print "_________INITIAL BOARD__________"
        print_board(board)
        print maylive, "may live"
        print maydie, "may die"
        print "starting first iteration"
        print "------------------------"
        
    
    initial_time = time.time()
    for iteration in range(iterations):
        starttime = time.time()
        #iterate over maylive and call Vivify
        for item in maylive:
            #Vivify items
            row,col = item
            if not board[row+1][col+1] and num_neighbors[row][col] == 3: #it's dead but should be alive
                board[row+1][col+1] = 1 #now it's alive
                newlive.append(item)
                
        for item in maydie:
            #Kill off items
            row,col = item
            if board[row+1][col+1] and (num_neighbors[row][col] < 2 or num_neighbors[row][col] > 3): #it's alive but should be dead
                board[row+1][col+1] = 0 #now it's dead
                newdie.append(item)
        if output:
            print_board(board)
            
        #Display the information for this iteration.  We have to do this before Add and Subtract neighbors
        #because they empty the newlive and newdie lists.
        changedstate = len(newlive)+len(newdie)
        print "iteration %s of %s" % (iteration+1, iterations)
        print len(newlive), "cells became alive"
        print len(newdie), "cells died"
        print changedstate, "cells changed state"
        
        
        maylive = []
        maydie = []
        for item in newlive:
            #Add neighbors
            live_row, live_col = item
            for row in range(live_row-1, live_row+2):
                for col in range(live_col-1, live_col+2):
                    #print row, col, live_row, live_col
                    if row < 0 or row >= width or col < 0 or col >= height or (row == live_row and col == live_col):
                        continue#skip out-of-bounds entries and the center
                    num_neighbors[row][col] += 1
                    if (num_neighbors[row][col]  == 3) and (board[row+1][col+1] == 0): #bring it back to life.
                        maylive.append((row, col))
                    elif (num_neighbors[row][col] == 4) and (board[row+1][col+1] == 1): #it's overcrowded, kill it off.
                        maydie.append((row,col))
                        
        
        for item in newdie:
            #Subtract neighbors
            dead_row, dead_col = item
            for row in range(dead_row-1, dead_row+2):
                for col in range(dead_col-1, dead_col+2):
                    if row < 0 or row >= width or col < 0 or col >= height or (row == dead_row and col == dead_col):
                        continue#skip out-of-bounds entries and the center
                    num_neighbors[row][col] -= 1
                    if num_neighbors[row][col] < 0: 
                        print "panic time in Subtract Neighbors!" # this should never happen.
                    
                    if num_neighbors[row][col]  == 3 and not board[row+1][col+1]: #bring it back to life.
                        maylive.append((row, col))
                    if num_neighbors[row][col] == 1 and board[row+1][col+1]: #it's undercrowded, kill it off.
                        maydie.append((row,col))
                        
        #let them know how long that iteration took.
        print "This iteration took %.3f milliseconds." % ((time.time() - starttime) * 1000)
        print "---------------------------------"
        newlive = []
        newdie = []
        
        
        if debug:
            #print the Neighbors table, it's helpful for debugging to make sure the values are set correctly.
            print "Neighbors:"
                       
            print  "_" * (len(num_neighbors) * 2 + 1)
            out = ""
        
            for row in num_neighbors:
                temp = ""
                for col in row:
                    temp += "|" + str(col)
                temp += "|\n"
                out += temp
        
            print out
            print "-----------------------"
        
        if debug:
          time.sleep(5)
    
    print "GoL 2 took %.3f seconds to run this configuration." % (time.time() - initial_time)
    
    
    
    
    
    
def gol1(board, width, height, iterations, debug=False, output=False):
    #the 1st gol simulation implementation
    
    #copy the old board so we make sure we don't accidentally change the original one.
    oldboard = copy.deepcopy(board)
    
    if output:
        print "_________INITIAL BOARD__________"
        print_board(oldboard)
        
    #get the starting time so we know how long algorithm takes to run.
    initial_time = time.time()
    
    for iteration in xrange(iterations):
        #keep track of # of cells that are changed
        changedcells = 0
        newboard = [[0 for i in range(width+2)] for i in range(height+2)]
        
        starttime = time.time()
        for rowindex,row in enumerate(oldboard[1:-1]):
            for colindex,col in enumerate(row[1:-1]):
                num = neighbors(oldboard, rowindex, colindex)
                if col: #it's alive
                    if num == 2 or num == 3: #stays alive
                        newboard[rowindex+1][colindex+1] = 1
                    else: #changing cell
                        changedcells += 1
                else:
                    if num == 3:
                        newboard[rowindex+1][colindex+1] = 1
                        changedcells += 1
        endtime = time.time()
        oldboard = newboard
        if output:
            print "-----------------------------------"
            if debug:
                print "\n"*80
            print_board(oldboard) 
            
        print "iteration %s of %s" % (iteration+1, iterations),";",changedcells, "cells changed; %.1f milliseconds." %((endtime-starttime)*1000)
        
        if debug:
            time.sleep(.5)
            
    print "GoL 1 took %.3f seconds to run this configuration." % (time.time() - initial_time)
    
    
    
def main():
    iterations = int(raw_input("Number of iterations: "))
    
    fname = raw_input("Filename of map to use (or press enter for random map): ")
    if fname.strip() == "":
        boardwidth = int(raw_input("Board Width: "))
        boardheight = int(raw_input("Board Height: "))
        probability = float(raw_input("Probability cell will be alive (float, range [0...1] ): "))
        #generate our random board by choosing items based upon the probability distribution the user enters.
        board = [[random.choice([1] * int((probability %1) * 100) + [0] * int((1-(probability%1)) * 100)) for i in range(boardwidth)] for i in range(boardheight)]
    else:
        board = []
        for line in open(fname):
            board.append([int(i) for i in line.strip()])
            
        boardwidth = len(board[0])
        boardheight = len(board)
    
    output = raw_input("Display boards (yes/no)? ").strip().lower() == "yes"
    debug = raw_input("Debug Mode (yes/no)? ").strip().lower() == "yes"
    
    f = file("temp.txt", "w")
    for line in board:
        f.write("".join([str(i) for i in line]))
        f.write('\n')
    f.close()
    
    #inflate board for hedge so the neighbors function works.
    boardwidth = len(board[0])
    boardheight = len(board)
    inflatedboard = [[0] * (boardwidth+2)]
    inflatedboard.extend([[0] + i + [0] for i in board])
    inflatedboard.extend([[0] * (boardwidth+2)])
    
    
    print "Running Game of Life 1..."
    gol1(inflatedboard, boardwidth, boardheight, iterations, debug=debug, output=output)
    raw_input("Done running Game of Life 1, press Enter to continue")
    print "Running Game of Life 2..."
    gol2(inflatedboard, boardwidth, boardheight, iterations, debug=debug, output=output)
    
    
if __name__ == "__main__":
    main()