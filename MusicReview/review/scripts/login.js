function testSubmit()
{
    // perform simple error-checking before submitting.
    
    // Grab the current value of the username field.
	row = document.getElementById("username").value;
    row = row.trim();
    // Do some error-checking.
    if (row.length == 0)
    {
		document.getElementById("error").innerHTML = "You must enter a username.";
        return false;
    }
	row = document.getElementById("password").value;
    row = row.trim();
    if (row.length == 0)
    {
		document.getElementById("error").innerHTML = "You must enter a password.";
        return false;
    }
    return true;
}