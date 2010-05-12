Virpobe Paireepinart
Project 2

Everthing works as it should.  If anything doesn't work / compile let me know please as it is probably due to a difference in configuration.
all my programs were tested and are hosted on firebird.

-----------

The first problem, the PHP table extension, is hosted online at
http://firebird.cs.txstate.edu/~vp1021/iip/hw2/problem1.php

It just goes through a couple of examples of testing out the table class to make sure all the methods work appropriately.
It's general php code so it could be hosted anywhere and work fine.

-----------

The second problem, the Pro*C program, is hosted online at
http://firebird.cs.txstate.edu/~vp1021/iip/hw2/problem2.php

you simply type in your query and hit enter.  the query will be submitted and the results displayed below.
you type your query into whichever box you want to search by.
for example, typing 'adam' into the Name box will return
Employee Name Salary Commission 
ADAMS 1100.00 0.00 

and typing 'accounting' into dept will return
Employee Name Salary Commission 
CLARK 2450.00 0.00 
KING 5000.00 0.00 
MILLER 1300.00 2500.00 

the other two fields should use numerical values.

in order to compile the pro*c program, you run the following command:
make -f demo_proc.mk sample2

note you must be on firebird in order for this to succeed.

Also, if you try to access the php file through the regular cs site,like http://cs.txstate.edu/~vp1021/iip/hw2/problem2.php,
it will not work, because it is unable to connect to the Oracle sql database.

