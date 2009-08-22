function testSubmit()
{
    // perform simple error-checking before submitting.
    
    // Grab the current value of the search field.
	row = document.getElementById("notes").value;
    row = row.trim();
    // Do some error-checking.
    if (row.length == 0)
    {
		document.getElementById("error").innerHTML = "You entered no notes.  Please enter at least 3 notes.";
        return false;
    }
    temp = row.split(' ');
    if (temp.length == 1)
    {
        document.getElementById("error").innerHTML = "You entered 1 note.  Please enter at least 3 notes.";
        return false;
    }
    else if (temp.length == 2)
    {
        document.getElementById("error").innerHTML = "You entered 2 notes.  Please enter at least 3 notes.";
        return false;
    }
    return true;
}