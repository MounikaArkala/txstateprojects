

function callScale()
{
	row = document.getElementById("notes").value;
    row = row.trim();
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
	page = "main";
	loadContent('content','scales.cgi');
}

function updateScales()
{
	groups = new Array();
    groupnum = document.getElementById("grps").value;
    var i = 0;
    for (i = 0; i < groupnum; i++)
    {
        groups[i] = document.getElementById("filter" + i).checked;
    }
	page = 'filtered';
	loadContent('scalesdiv', 'scales.cgi');
}
