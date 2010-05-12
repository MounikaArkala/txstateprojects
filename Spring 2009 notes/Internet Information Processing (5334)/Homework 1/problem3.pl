#!/usr/bin/perl
##
## Homework 1 Problem 3 by Virpobe Luke Paireepinart
## for Internet Information Processing, Spring 2010, Texas State University
##
print "Content-type: text/plain; charset=iso-8859-1\n\n";

#read in file...
$data_file = "input.txt";
$ret = open(DAT, $data_file);
if (!$ret)
{
    print "Could not open $data_file!  Are you sure it exists in the proper folder?";
    die("Could not open $data_file!");
}
@text = <DAT>;

#keep list of all words w/ uppercase letters in %uppercase associative array.
%uppercase = ();
foreach $var (@text) {
    foreach $word ($var =~ m/([A-Z][a-zA-Z]+)/g)
    {
        $uppercase{$word} += 1;
    }
}

#use the associative array to print the words.
foreach $var (sort(keys(%uppercase))) {
    $val = $uppercase{$var};
    print "$var: $val\n";
}

#show em what the input was...
print "\n\n";
print "Original Text\n";
print "------------------------------\n";
foreach $var (@text) {
    print "$var";
}
