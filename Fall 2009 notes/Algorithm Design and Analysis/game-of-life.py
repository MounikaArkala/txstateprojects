
import copy, random, time

def print_board(board, size):
    print  "_" * (size * 2 + 1)
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
    row += 1
    col += 1
    return sum([sum(board[row-i][col-1:col+2]) for i in range(-1,2)]) - board[row][col]

def gol1(board,iterations):
    boardsize = len(board) - 2
    oldboard = copy.deepcopy(board)
    for i in range(iterations):
    
        print "\n"*80
        print_board(oldboard, )
        print "Current: %s, Final %s" % (i+1, iterations)
        print neighbors(board, 0,0)
        time.sleep(1)
    #start w/ a random configuration.
    
    
def main():
    n = 25
    board = [[0] * (n+2)]
    board.extend([[0] + [random.choice([1,0]) for i in range(n)] + [0] for i in range(n)])
    board.extend([[0] * (n+2)])
    gol1(board,1)
    
    
if __name__ == "__main__":
    main()