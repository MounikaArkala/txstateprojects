


======== INTRODUCTION =========
This is Project 1 for Crafting Compilers at Texas State University, Spring 2009
Due on February 12th, for prof. Quasem.
The team consists of Virpobe Paireepinart.

The program is a scanner, the first stage of a compiler chain.
In this instance I wrote the compiler in Python.  The configuration file
'config.py' has some options that can be configured, and my scanner
is nearly as flexible as "lex", but does no code generation.
You directly define the regular expressions in 'config.py'
and provide a callback function if that RE is the matching one.
The scanner will then take care of parsing the input and calling the callback functions.


========  IMPORTANT ==========

There is an option in 'config.py' called "debug" that makes the output of the tokens easier to read.
If you only want to see the tokenized output (eg. you want to only see "253" but not that 253 is the keyword 'if')
then turn off debug mode.  I left debug on because I think it makes the output easier to read.
NOTE: the correct way to enable/disable debug mode is to set the 'debug' variable to True or False.  This is
case-sensitive so don't use true and false as it will cause an error.



========  TODO =========
The program is feature-complete as per the specification document.
There are no known errors.  There are however a few additional features I'd like to add
(eg. actual exceptions rather than printing "ERROR:") and I will add these when I connect the scanner
and the parser together.




======== RUNNING THE EXAMPLE CODE ========
One good thing about Python programs is that there's no need to compile them.

I've included my example test.c program that I've been parsing.

Simply execute the command

python scanner.py test.c


in the same directory as the code and it will scan.
