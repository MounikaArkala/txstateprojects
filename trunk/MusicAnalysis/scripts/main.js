/* Main.js
------------------------------
Author:    Luke Paireepinart
Copyright: Nico Schüler

Texas State University
Summer 2009
------------------------------
Brief Summary:
This is the Javascript file that contains all the similar functionality between the
different programs on MusicAnalysis.  
*/

/*
===============================
=    "Borrowed" Functions     =
===============================
*/
String.prototype.trim = function()
{
    /*
    Purpose: remove whitespace from beginning and end of a string.
    Notes: adds its method to the base String class so you can just use
    the .trim() method on any string.    */
	return this.replace(/^\s+|\s+$/g,"");
}
String.prototype.ltrim = function()
{
    /*
    Purpose: remove whitespace from beginning of a string.
    Notes: adds its method to the base String class so you can just use
    the .trim() method on any string.    */
	return this.replace(/^\s+/,"");
}
String.prototype.rtrim = function() 
{
    /*
    Purpose: remove whitespace from end of a string.
    Notes: adds its method to the base String class so you can just use
    the .trim() method on any string.    */
	return this.replace(/\s+$/,"");
}

function GetXmlHttpObject()
{
    /*
    Purpose: provide an XmlHttpObject in a generic fashion
    Notes: necessary for compatibility with older (MSIE) browsers.    */
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


/*
===============================
=   MusicAnalysis Functions   =
===============================
*/

function load()
{
    /*
    Purpose: load main page into "content" div upon end of loading of index.html's body.
    */
    loadContent("content", "main.html");
    row = "A"; // just a sensible default.
}

function handleEnter(event, func)
{
    /*
    Purpose: a very simple wrapper that will call a function if
    event's key is the same as the keyboard "enter" button.  */
	var key = event.keyCode || event.which;
	if (key == 13)
	{
		func();
	}
}

function loadContent(divName, pageName)
{	
    /*
    Purpose: load content from a specific page (pageName) via AJAX into a specific container (divName).
    Notes: this is the main function for loading AJAX content.
    Relies on loadingLoaded as its callback for the AJAX load, and
    on genArgs to create the argument list.  */
	target = divName;
	xmlhttp = GetXmlHttpObject();
	newUrl = pageName;
	newUrl = newUrl + genArgs(pageName);
	if (xmlhttp == null)
	{
		alert ("Your browser does not support XMLHTTP!");
		return;
	}
    // load the "loading" page, and when that page is done loading,
    // loadingLoaded will start loading the requested page.
	var url = "loading.html";
	xmlhttp.onreadystatechange = loadingLoaded;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}


function loadingLoaded()
{
    /*
    Purpose: start an AJAX call to load content into a container.
    Notes: relies on contentChanged to load the actual content.
    The main reason this function exists is just to put up a "loading"
    animation while we wait for the page to load.  Could really just display a "loading"
    message somewhere on screen until the loading is done.  */
    
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

function contentChanged()
{
    /*
    Purpose: AJAX callback for a state change of a page load request
    Notes: "target" global variable should be set to the div you want to load a page into.
    Otherwise it'll load into the "content" div by default.    */
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
    /*
    Purpose: append the arguments to a page request.
    Notes: Centralizes all argument passing to one method.
    This allows all the other functions to be more generic.    */
    
    var args = "?";
    
    // an if/elif block for each page that requires arguments.
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
			args = args + "notes=" + escape(row) + "&page=" + escape(page) + "&order=" + escape(order) + "&consecutive=" + escape(consecutive);
		}
		else if (page == "filtered")
		{
            // Need to grab the filter statuses and append them to the request
            // so the server knows which values to filter out.
			args = args + "notes=" + escape(row) + "&page=" + escape(page) + "&order=" + escape(order) + "&consecutive=" + escape(consecutive);
			for (i = 0; i < groupnum; i++)
			{
				args = args + "&filter"+i+"="+ escape(groups[i]);
			}
		}
		
	}
    
	else
	{
        // No page-specific arguments so just return an empty string.
		return "";
	}
    
    // There were some page-specific arguments so return them.
	return args;
}
