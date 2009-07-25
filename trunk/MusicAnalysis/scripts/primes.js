/* Primes.js
------------------------------
Author:    Luke Paireepinart
Copyright: Nico Schüler

Texas State University
Summer 2009
------------------------------
Brief Summary:

A few routines for error-checking and getting the correct values set up for passing to the
back-end Python script.
*/

function callPrime()
{
    /*
    Purpose: submit the 12-tone row to be processed to the backend script.
    Notes: also performs simple error-checking before submitting.  */
    
    // Grab the current value of the search field.
	row = document.getElementById("notes").value;
    row = row.trim();
    
    // Do some error-checking.
    if (row.length == 0)
    {
		document.getElementById("error").innerHTML = "You entered no notes.  Please enter exactly 12 notes.";
        return false;
    }
    var temp = new Array();
    temp = row.split(' ');
    // Tone rows need to be 12 items long.
    if (temp.length != 12)
    {
        if (temp.length == 1)
        {
            document.getElementById("error").innerHTML = "You entered 1 note.  Please enter exactly 12 notes.";
        }
        else
        {
            document.getElementById("error").innerHTML = "You entered " + temp.length + " notes.  Please enter exactly 12 notes.";
        }
        return false;
    }
    
    
    // passed error checking so load content.
	page = "main";
	loadContent('content','primes.cgi');
}

function callOD()
{
    /*
    Purpose: do a search for a specific Order-Dependent entry in the 12-tone matrix.  */
	series = document.getElementById("odseries").value;
	wrap = document.getElementById("wraparound").checked;
	page = "od";
	loadContent('primesdiv','primes.cgi');
}

function callOID()
{
    /*
    Purpose: do a search for a specific Order-Independent entry in the 12-tone matrix.  */
	series = document.getElementById("oidseries").value;
	wrap = document.getElementById("wraparound").checked;
	page = "oid";
	loadContent('primesdiv','primes.cgi');
}
