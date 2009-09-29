/* Chords.js
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


function testSubmit()
{
    // perform simple error-checking before submitting.
    
    // Grab the current value of the search field.
	row = document.getElementById("notes").value;
    row = row.trim();
    // Do some error-checking.
    if (row.length == 0)
    {
		document.getElementById("error").innerHTML = "You entered no notes.  Please enter at least 2 notes.";
        return false;
    }
    temp = row.split(' ');
    if (temp.length == 1)
    {
        document.getElementById("error").innerHTML = "You entered 1 note.  Please enter at least 2 notes.";
        return false;
    }
    return true;
}
