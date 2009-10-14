# Virpobe Paireepinart 2009 Texas State University Algorithms
# this is a solution for the 8-queens problem
#TODO: Comment this!
import random, time
def print_board(board):
    print  "_" * (len(board) * 2 + 1)
    for i in board:
        if i >= 0:
            out = i * "|_" + "|Q" + (len(board) - i - 2) * "|_"
        else:
            out = i * "|_" + "|_" + (len(board) - i - 2) * "|_"
        if i == len(board) - 1:
            out += "|"
        else:
            out += "|_|"
        print out
        
        
BOARDSIZE = 16
DIAGONAL = (2*BOARDSIZE-1)
DOWNOFFSET = BOARDSIZE-1

queencol = [-1]*BOARDSIZE
colfree = [True] * BOARDSIZE
upfree = [True] * DIAGONAL
downfree = [True] * DIAGONAL
output_boards = False
queencount = -1
numsol = 0
numcalls = 0

def AddQueen():
    global BOARDSIZE, DIAGONAL, DOWNOFFSET, queencol, colfree, upfree, downfree, queencount, numsol, numcalls, output_boards
    queencount += 1
    numcalls += 1
    for col in range(BOARDSIZE):
        if (colfree[col] and upfree[queencount + col] and downfree[queencount - col + DOWNOFFSET]):
            #Put a queen in position (queencount, col).
            queencol[queencount] = col
            colfree[col] = False
            upfree[queencount + col] = False
            downfree[queencount - col + DOWNOFFSET] = False
            if (queencount == BOARDSIZE-1): #termination condition
                #print_board(queencol)
                numsol += 1
                if output_boards:
                    print_board(queencol)
            else:
                AddQueen() # Proceed recursively.
            #Now backtrack by removing the queen.
            colfree[col] = True
            upfree[queencount + col] = True
            downfree[queencount - col + DOWNOFFSET] = True
        
    queencount -= 1
    

def main():
    global BOARDSIZE, DIAGONAL, DOWNOFFSET, queencol, colfree, upfree, downfree, queencount, numsol, numcalls, output_boards
    for boardsize in range(4,17):
        BOARDSIZE = boardsize
        DIAGONAL = (2*BOARDSIZE-1)
        DOWNOFFSET = BOARDSIZE-1
        numsol = 0
        queencol = [-1]*BOARDSIZE
        colfree = [True] * BOARDSIZE
        upfree = [True] * DIAGONAL
        downfree = [True] * DIAGONAL
        queencount = -1
        #print "%s, %s, %s, %s" % (boardsize, numcalls, numsol, calculation_time)
        print "==========================================="
        print "Calculating %sx%s board with %s queens" % (boardsize, boardsize, boardsize)
        print "==========================================="
        choice = raw_input("Run with solution boards displayed (yes/no)? ")
        if choice.lower().strip() == "yes":
            output_boards = True
        else:
            output_boards = False
        current = time.time()
        AddQueen()
        calculation_time = time.time() - current
        print "AddQueen was called %s times. %s solutions were found." % (numcalls, numsol)
        print 
        print
    print "End!"

    
if __name__ == "__main__":
    main()
    