
function callPrime()
{
	row = document.getElementById("notes").value;
    row = row.trim();
    if (row.length == 0)
    {
		document.getElementById("error").innerHTML = "You entered no notes.  Please enter exactly 12 notes.";
        return false;
    }
    var temp = new Array();
    temp = row.split(' ');
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
	page = "main";
	loadContent('content','primes.cgi');
}

function callOD()
{
	series = document.getElementById("odseries").value;
	wrap = document.getElementById("wraparound").checked;
	page = "od";
	loadContent('primesdiv','primes.cgi');
}

function callOID()
{
	series = document.getElementById("oidseries").value;
	wrap = document.getElementById("wraparound").checked;
	page = "oid";
	loadContent('primesdiv','primes.cgi');
}
