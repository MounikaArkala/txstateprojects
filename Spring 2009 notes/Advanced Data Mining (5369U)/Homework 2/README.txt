Virpobe Paireepinart
Advanced Data Mining
Spring 2010 Texas State University

Execution
--------
I included the file 'kmeans' as both 'kmeans' and 'kmeans.py'.  They are both the same file,
but to conform to the program execution specified in the homework document I chose to include 'kmeans' as well.
kmeans.py can be executed like so:
python kmeans.py k infile

And the kmeans version can be executed as specified in the homework document.
./kmeans k infile

If this gives you a permissions errors just do
chmod 755 kmeans

and attempt to run it again.

This has been tested & works fine on the school Linux computers.  If your python install is located somewhere besides
/usr/bin/python then you need to change line 1 of the kmeans file to be directed at your Python install.
Or, an easier alternative: just run the program the first way (python kmeans.py k infile).

This program was implemented in Windows 7 64 bit using 32 bit Python 2.6.  However it should work
on pretty much any platform and most versions of Python 2.x.
