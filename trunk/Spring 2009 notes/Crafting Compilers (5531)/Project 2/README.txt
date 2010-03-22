Assignment 2 by Luke Paireepinart, Texas State University, Spring 2010


~~~ Setup ~~~
In order to run the program you need a Python version of 2.4 or greater.
The school's linux computers have this.

I reimplemented the scanner in PLY and it's included in the mcc file now.

The program uses PLY (python lex/yacc) and PyDOT (python graphviz library)
but I have included these in the redistributable.

In order to generate the SVG graph files, you must have graphviz installed.
It can be downloaded and installed here:  http://www.graphviz.org/Download..php

After you install it you must change the dotpath in mcc.py.
It is near the top of the file.
Alter it to be the absolute path to the dot.exe file in your graphviz.


In order to view the graphviz files, you can drag the .svg files into Firefox,
or you can install Inkscape (can be found here: http://www.inkscape.org/download/?lang=en )
Once it's installed, just open the .svg files with inkscape.


~~~ Running ~~~
You don't have to compile it, it's Python :)
Simply run it with the correct parameters.
All you need to specify is the input .c file and the output .svg file.
Here is an example:
C:\Project 2>python mcc.py examples/bigfile.c graphs/bigfile.svg

0 lexer errors and 0 syntax errors occurred.
drawing graph...
graph drawn.


~~~ Example of error'd file ~~~
C:\Project 2>python mcc.py examples/errs1.c graphs/errs1.svg

Syntax Error: Redefinition of global foo with type char (originally type int) near line 16.

Syntax Error: Redefinition of global foo with type int near line 17.

Syntax Error: Redefinition of local variable j with type int near line 21.

Syntax Error: Redefinition of global foo with type int near line 41.

Lexer Error: Unterminated String Constant at Line 46 Column 14.

Lexer Error: Illegal character '!' at line 46 column 19.

SyntaxError: Variable "Jeff" is undefined near line 45.

Lexer Error: Unterminated comment at line 52 column 2.

Syntax Error: Undefined identifier unterminated near line 52.

Syntax Error: Undefined identifier comment near line 52.

Syntax Error: Redefinition of global foo with type string (originally type int) near line 51.

3 lexer errors and 8 syntax errors occurred.
As some errors occurred, the tree is probably not correct.
There is some chance that it will still be able to be rendered correctly, but it is not guaranteed.
drawing graph...
graph drawn.


--- The tree did manage to render, but it may not be very helpful.

~~~ Notes ~~~
I have included sample graphs in the graphs/ directory.
I would suggest taking the effort to get graphviz and inkscape installed / configured.
I tried to ensure it will still work without these programs but one can never be certain of such things.

~~~ Known Bugs / Limitations ~~~
It doesn't seem to process the error of a missing right brace correctly.
Most other syntax errors seemed fine.
