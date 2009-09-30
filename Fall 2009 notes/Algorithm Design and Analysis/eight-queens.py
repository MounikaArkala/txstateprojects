# Virpobe Paireepinart 2009 Texas State University Algorithms
# this is a solution for the 8-queens problem

import random

def print_board(board):
    print  "_" * (len(board) * 2 + 1)
    for i in board:
        out = i * "|_" + "|Q" + (len(board) - i - 2) * "|_"
        if i == len(board) - 1:
            out += "|"
        else:
            out += "|_|"
        print out

 
def queens(size):
    print "Investigating a board of %s by %s with %s queens." % (size, size, size)
    counter = 0
    # TODO: rewrite this, it has to use the AddQueen function he specified in the notes.
    print "Starting with a random permutation of queens."
    board = [i for i in range(size)]
    random.shuffle(board)
    print_board(board)

queens(8)