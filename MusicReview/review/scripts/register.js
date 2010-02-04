function testSubmit()
{
    // TODO: finish off the error checking.
    
    
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
    if (row.length <= 3)
    {
		document.getElementById("error").innerHTML = "You must enter a password >= 4 characters long.";
        return false;
    }
    
	if (!checkInputLength('lname', 'Last Name', 0))  return false;
    
    return true;
}

function checkInputlength(name, desc, len)
{
    
	row = document.getElementById(name).value;
    row = row.trim();
    // Do some error-checking.
    if (row.length <= len)
    {
        if (len == 0)
        {
            document.getElementById("error").innerHTML = "You must enter a " + desc + ".";
        }
        else
        {
            newlen = len+1;
            document.getElementById("error").innerHTML = "You must enter a "+desc+" >= "+newlen+" characters long.";
        }
        return false;
    }
    return true;
}