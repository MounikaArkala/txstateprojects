Virpobe Paireepinart
CS 5338
Texas State University
Fall 2009

The program can be run by starting pass.py in the current directory,
such as
./pass.py

if on linux,
or just double-clicking in windows.
You must have Python installed (it's installed by default on the Linux boxes provided by the school and on Mac OS, for Windows you can get it from http://www.python.org (Version 2.6))


Once the program is started, simply follow the on-screen instructions.
For example, if you have an input document that is a rip of the HTML (such as in.txt provided with the program)
just type "in.txt" when asked if you want to use an input file.
When asked for an output file, you can specify an output file or just hit enter to output to standard out.
Example:


**************************************
Input file (or leave blank for automatic retrieval): in.txt
Output file (or leave blank for stdout):
--------------------------------------
You have chosen to process an input file (in.txt).
--------------------------------------
Name: Javier Arellano
Position: Adjunct Faculty
Education: Unknown
Research Interest 1: unknown
Email: ja32@txstate.edu
Webpage: http://www.cs.txstate.edu/~ja32/
--------------------------------------
Input file done processing, exiting.
thank you for using the program!
**************************************


If you don't want ot use an Input file, the program will automatically download the page from the internet
that contains all of the faculty, and parse it and show you a list of all of the faculty.
Example:


**************************************
Input file (or leave blank for automatic retrieval):
Output file (or leave blank for stdout):
This is a list of all professors on campus.
Moonis Ali (Professor)
Javier Arellano (Adjunct Faculty)
Xiao Chen (Associate Professor)
Sumit DasGupta (Adjunct Faculty)
Wilbon Davis (Professor)
H. John Durrett (Associate Professor)
Ju (Byron) Gao (Assistant Professor)
Qijun Gu (Assistant Professor)
Mina S. Guirguis (Assistant Professor)
Carol Hazlewood (Assistant Department Chair, Associate Professor)
James Holt (Adjunct Faculty)
C. Jinshong Hwang (Professor)
Khosrow Kaikhah (Associate Professor, Graduate Advisor)
Lee Koh (Senior Lecturer)
Oleg Komogortsev (Assistant Professor)
Yijuan (Lucy) Lu (Assistant Professor)
Thomas McCabe (Associate Professor)
Mark McKenney (Assistant Professor)
Carl Mueller (Assistant Professor)
Anne Ngu (Associate Professor)
Wuxu Peng (Professor)
Rodion Podorozhny (Assistant Professor)
Roger Priebe (Senior Lecturer, Faculty Advisor)
Apan Qasem (Assistant Professor)
Becky Reichenau (Senior Lecturer)
Ronald Sawey (Associate Professor)
Stephen Seidman (Dean, College of Science , Professor, Computer Science)
Dan Tamir (Assistant Professor)
--------------------------------------
Search:
**************************************


Simply type a search to rip that professor's data.  Note that some professors do not have complete data (such as the adjunct professors) so it will just get all possible data it can and put "unknown" for any fields it can't determine.

When you type in a search it uses a regex to match your keywords to every name, so for example if you type o k you will find all professors with either an o or k (or both) in their name, and if you type "oleg" you will automatically select Oleg Komogortsev
(it auto-selects anytime a search only has a single result.)



**************************************
Search: o k
That query matched the following people:
Rodion Podorozhny
Thomas McCabe
H. John Durrett
Khosrow Kaikhah
Moonis Ali
Oleg Komogortsev
Lee Koh
Ju (Byron) Gao
Javier Arellano
Ronald Sawey
Xiao Chen
Wilbon Davis
Becky Reichenau
James Holt
Carol Hazlewood
C. Jinshong Hwang
Roger Priebe
Mark McKenney
Please use a more restrictive query.

Search: oleg
--------------------------------------
You have chosen to process Oleg Komogortsev.
--------------------------------------
Name: Oleg Komogortsev
Position: Assistant Professor
Education: BS Volgograd State University; MS, PhD Kent State University
Research Interest 1: human computer interaction
Research Interest 2: visual perception
Research Interest 3: multimedia
Research Interest 4: and networking
Email: ok11@txstate.edu
Webpage: http://www.cs.txstate.edu/~ok11
--------------------------------------
Hint: if you are finished, type 'exit'.
Search:
**************************************


Also, if you specify an input file taht doesn't exist, it will prompt you for one that does, and if you try to output to a file that
exists already you can choose to overwrite the data or just append it.
The sample output file I have provided has several professor's information appended.

Example:

**************************************
Input file (or leave blank for automatic retrieval):
Output file (or leave blank for stdout): out.txt
This is a list of all professors on campus.
[snip list]
--------------------------------------
Search: mccabe
--------------------------------------
You have chosen to process Thomas McCabe.
--------------------------------------
Sending output to disk (out.txt).
File out.txt already exists on disk.  Do you want to (append) or (overwrite)?
appppppend
I did not understand your response, please try again!
File out.txt already exists on disk.  Do you want to (append) or (overwrite)?
append
File output successful!
--------------------------------------
Hint: if you are finished, type 'exit'.
Search: exit
thank you for using the program!
**************************************

I think it works pretty well :)