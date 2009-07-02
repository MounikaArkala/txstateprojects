/* Other People's Functions */

String.prototype.trim = function() {
	return this.replace(/^\s+|\s+$/g,"");
}
String.prototype.ltrim = function() {
	return this.replace(/^\s+/,"");
}
String.prototype.rtrim = function() {
	return this.replace(/\s+$/,"");
}


function GetXmlHttpObject()
{
	if (window.XMLHttpRequest)
	{
		// code for IE7+, Firefox, Chrome, Opera, Safari
	return new XMLHttpRequest();
	}
	if (window.ActiveXObject)
	{
		// code for IE6, IE5
		return new ActiveXObject("Microsoft.XMLHTTP");
	}
	return null;
}


/* generic updating callback */
function contentChanged()
{
	if (target == null)
	{
		target = "content";
	}
	if (xmlhttp2.readyState==4)
	{
		document.getElementById(target).innerHTML = xmlhttp2.responseText;
	}
}


function genArgs(pageName)
{
    var args = "?";
	if (pageName == "primes.cgi")
	{
		if (page == "main")
		{
			args = args + "notes=" + escape(row);
			args = args + "&page=" + escape(page);
		}
		else if (page == "od" || page == "oid")
		{
			args = args + "notes=" + escape(row);
			args = args + "&series=" + escape(series);
			args = args + "&wrap=" + escape(wrap);
			args = args + "&page=" + escape(page);
		}
		
	}
	else if (pageName == "scales.cgi")
	{
		if (page == "main")
		{
			args = args + "notes=" + escape(row) + "&page=" + escape(page);
		}
		else if (page == "filtered")
		{
			args = args + "notes=" + escape(row) + "&page=" + escape(page);
			for (i = 0; i < groupnum; i++)
			{
				args = args + "&filter"+i+"="+ escape(groups[i]);
			}
		}
		
	}
	else
	{
		return "";
	}
	return args;
}
		
function loadingLoaded()
{
	if (target == null)
	{
		target = "content";
	}
	if (xmlhttp.readyState==4)
	{
        xmlhttp2=GetXmlHttpObject();
		document.getElementById(target).innerHTML = xmlhttp.responseText;
        xmlhttp2.onreadystatechange = contentChanged;
        xmlhttp2.open("GET",newUrl,true);
        xmlhttp2.send(null);
	}
}

function loadContent(divName, pageName)
{	
	target = divName;
	xmlhttp=GetXmlHttpObject();
	newUrl = pageName;
	newUrl = newUrl + genArgs(pageName);
	if (xmlhttp == null)
	{
		alert ("Your browser does not support XMLHTTP!");
		return;
	} 
	var url = "loading.html";
	xmlhttp.onreadystatechange = loadingLoaded;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
    /*
	xmlhttp.onreadystatechange = contentChanged;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);*/
	
}

function load()
{
    loadContent("content", "main.html");
    row = "A";
}

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


function loadOD()
{
	series = document.getElementById("odseries").value;
	wrap = document.getElementById("wraparound").checked;
	page = "od";
	loadContent('primesdiv','primes.cgi');
}

function loadOID()
{
	series = document.getElementById("oidseries").value;
	wrap = document.getElementById("wraparound").checked;
	page = "oid";
	loadContent('primesdiv','primes.cgi');
}

function handleEnter(event, func)
{
	var key = event.keyCode || event.which;
	if (key == 13)
	{
		func();
	}
}