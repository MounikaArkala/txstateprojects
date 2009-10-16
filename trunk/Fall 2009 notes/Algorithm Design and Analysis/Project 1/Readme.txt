
Python programs do not need to be compiled so no setup steps need to be taken.  You can view the source and run it directly.

Each program can be run by typing

python eight-queens.py

and

python game-of-life.py


They can be run this way on the Linux servers by default (already have python installed.)
If you are testing on your home computer, install Python 2.6, then start a command line in the same directory as the scripts,
and type the commands above.


----------------------------------


How to use eight-queens.py

- when you start the program it will run through 4x4 to 16x16 boards.
- on each board it will ask you if you want to see the solutions or not.
- in either case you will get output of the number of calls to AddQueen and the number of solutions found.

----------------------------------

How to use game-of-life.py
you first choose the # of iterations
then it will go through the task of generating a board (or using a board file that already exists)
 - if you want to load a board, type the name of the file (eg. map1.txt, map2.txt ... map4.txt)
 - if you want to generate a board, just hit "enter"
    - if you're generating a board, you must specify the width and the height (doesn't need to be square) and the density.
      @ a density of 1 means every square is occupied, and a density of 0 means no squares are occupied.  use values in between these two.
you will then be asked if you want to display boards.  This will display the board for every iteration.
Then you will be asked for debug mode.  Debug mode contains sleeps between board displays, and outputs more information that may be useful.