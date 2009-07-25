/* Scales.js
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


function callScale()
{
    /*
    Purpose: performing a non-ordered search (continuity of notes based on "consecutive" checkbox).
    Notes: also performs simple error-checking before submitting.  */
    
    // Set the search to non-ordered.
    order = false;
    
    // Grab the current value of the search field.
	row = document.getElementById("notes").value;
    row = row.trim();
    // check whether search is consecutive.
    consecutive = document.getElementById("consecutive").checked;
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
    // passed error checking so load content.
	page = "main";
	loadContent('content','scales.cgi');
}

function callScaleOrdered()
{
    /*
    Purpose: performing an ordered search (continuity of notes based on "consecutive" checkbox).
    Notes: also performs simple error-checking before submitting.  */
    
    // Set the search to ordered.
    order = true;
    
    // Grab the current value of the search field.
	row = document.getElementById("ordered_notes").value;
    row = row.trim();
    // check whether search is consecutive.
    consecutive = document.getElementById("consecutive").checked;
    
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
    // passed error checking so load content.
	page = "main";
	loadContent('content','scales.cgi');
}

function updateScales()
{
    /*
    Purpose: update scale with new filter settings.
    Notes: some assumptions made about sorting order of filters but
    there wasn't an easy way to avoid it.  */
	groups = new Array();
    groupnum = document.getElementById("grps").value;
    var i = 0;
    for (i = 0; i < groupnum; i++)
    {
        groups[i] = document.getElementById("filter" + i).checked;
    }
    // load the page again with the filter set correctly.
	page = 'filtered';
	loadContent('scalesdiv', 'scales.cgi');
}
