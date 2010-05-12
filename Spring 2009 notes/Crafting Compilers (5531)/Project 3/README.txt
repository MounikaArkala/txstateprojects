Assignment 3 by Luke Paireepinart, Texas State University, Spring 2010


~~~ Setup ~~~
In order to run the program you need a Python version of 2.4 or greater.
The school's linux computers have this.

The scanner / parser are the same as assignment 2 but extended a bit.

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

~~~ Notes ~~~
I have included sample graphs in the graphs/ directory.
I would suggest taking the effort to get graphviz and inkscape installed / configured.
I tried to ensure it will still work without these programs but one can never be certain of such things.

IMPORTANT: I may have deviated from the spec, because I keep a local scope of each function, and pop it into a variable that collects each function's local scope, so I don't have just 'local' and 'global' variables, I have 'global' variables and then variables that are local to a specific function.  This leads to a different error than specified for one of the test programs but it still catches the error (defining a local variable in one function and using it in another).

~~~ Known Bugs / Limitations ~~~
None as far as I know, but unfortunately I was not able to extensively test everything.
It catches every error in all 12 sample items, but probably has some other errors.
I added as much information as I could to the AST, but it's not rendered in the output graphs.
I am not sure what information should be included in the AST 'cause I'm not sure what we're going to do with it at the next step exactly, so I will likely fix / add / remove stuff from the AST.  But it does work so far.  For example, all function signatures are attached to all the function nodes, and a subtype 'array' is attached to any variable of type array.  Things like that are already implemented.



~~~ Example ~~~
Here is a run on all 12 test files
C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test0.c graphs/test0.svg

Syntax Error: Redefinition of local variable i with type int near line 5.

======================
Global scope:  []
Local Scopes:  {'foo': [('int', 'i'), ('int', 'k')]}
======================
0 lexer errors and 1 syntax errors occurred.

As some errors occurred, the tree is probably not correct.
There is some chance that it will still be able to be rendered correctly, but it is not guaranteed.
drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test1.c graphs/test1.svg

Syntax Error: Variable "j" is undefined near line 6.

======================
Global scope:  []
Local Scopes:  {'foo': [('int', 'k'), ('int', 'i')]}
======================
0 lexer errors and 1 syntax errors occurred.

As some errors occurred, the tree is probably not correct.
There is some chance that it will still be able to be rendered correctly, but it is not guaranteed.
drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test2.c graphs/test2.svg

Syntax Error: Undefined Function bar near line 6.

======================
Global scope:  []
Local Scopes:  {'foo': [('int', 'k'), ('int', 'i')]}
======================
0 lexer errors and 1 syntax errors occurred.

As some errors occurred, the tree is probably not correct.
There is some chance that it will still be able to be rendered correctly, but it is not guaranteed.
drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test3.c graphs/test3.svg

Syntax Error: Function foo re-declared near line 11.

======================
Global scope:  []
Local Scopes:  {'foo': [('int', 'k'), ('int', 'i')]}
======================
0 lexer errors and 1 syntax errors occurred.

As some errors occurred, the tree is probably not correct.
There is some chance that it will still be able to be rendered correctly, but it is not guaranteed.
drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test4.c graphs/test4.svg

Syntax Error: Illegal Array Index with variable c of type char near line 7.

======================
Global scope:  []
Local Scopes:  {'foo': [('char', 'c'), ('int', 'a')]}
======================
0 lexer errors and 1 syntax errors occurred.

As some errors occurred, the tree is probably not correct.
There is some chance that it will still be able to be rendered correctly, but it is not guaranteed.
drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test5.c graphs/test5.svg

Syntax Error: Illegal assignment of variable i of type int to variable c of type char near line 6.

======================
Global scope:  []
Local Scopes:  {'foo': [('char', 'c'), ('int', 'i')]}
======================
0 lexer errors and 1 syntax errors occurred.

As some errors occurred, the tree is probably not correct.
There is some chance that it will still be able to be rendered correctly, but it is not guaranteed.
drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test6.c graphs/test6.svg

Syntax Error: Too few parameters to function foo around line 7.
:
======================
Global scope:  []
Local Scopes:  {'foo': [('int', 'i')], 'bar': []}
======================
0 lexer errors and 0 syntax errors occurred.

drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test7.c graphs/test7.svg

Syntax Error: Too many parameters to function foo around line 7.

======================
Global scope:  []
Local Scopes:  {'foo': [('int', 'i')], 'bar': []}
======================
0 lexer errors and 1 syntax errors occurred.

As some errors occurred, the tree is probably not correct.
There is some chance that it will still be able to be rendered correctly, but it is not guaranteed.
drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test8.c graphs/test8.svg

Syntax Error: Function foo expects int (not char) as parameter 1 around line 8.

======================
Global scope:  []
Local Scopes:  {'foo': [('int', 'i')], 'bar': [('char', 'c')]}
======================
0 lexer errors and 1 syntax errors occurred.

As some errors occurred, the tree is probably not correct.
There is some chance that it will still be able to be rendered correctly, but it is not guaranteed.
drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test9.c graphs/test9.svg

Warning : Shadowing global variable i near line 4.

======================
Global scope:  [('int', 'i')]
Local Scopes:  {'foo': [('int', 'i')]}
======================
0 lexer errors and 0 syntax errors occurred.

drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test10.c graphs/test10.svg

======================
Global scope:  [('int', 'i')]
Local Scopes:  {'foo': []}
======================
0 lexer errors and 0 syntax errors occurred.

drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test11.c graphs/test11.svg

Syntax Error: Variable "i" is undefined near line 7.

======================
Global scope:  []
Local Scopes:  {'foo': [('int', 'i')], 'bar': []}
======================
0 lexer errors and 1 syntax errors occurred.

As some errors occurred, the tree is probably not correct.
There is some chance that it will still be able to be rendered correctly, but it is not guaranteed.
drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>python mcc.py testcode/test12.c graphs/test12.svg

======================
Global scope:  []
Local Scopes:  {'foo': [('int', 'x')]}
======================
0 lexer errors and 0 syntax errors occurred.

drawing graph...
graph drawn.

C:\Projects\Spring 2009 notes\Crafting Compilers (5531)\Project 3>