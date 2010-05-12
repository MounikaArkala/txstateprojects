#!/usr/bin/perl
##
## Homework 1 Problem 4 by Virpobe Luke Paireepinart
## for Internet Information Processing, Spring 2010, Texas State University
##

#Perl function for trimming whitespace, from perl doc's.
sub trim($)
{
	my $string = shift;
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	return $string;
}

#start out with our input string (change this if you want a different string.
$str = "alfred=good & betsy=&juno=ok&ben=&suko=mediocre&jefferson=terrible";

print "Content-type: text/plain; charset=iso-8859-1\n\n";
print "original string: $str\n";

#split on &....
@pairs = split("&", $str);
foreach $word (@pairs)
{
    #for each pair, split on =.
    @pair = split("=", $word);
    $name = trim($pair[0]);
    $val = trim($pair[1]);
    print "$name is $val\n";
}
