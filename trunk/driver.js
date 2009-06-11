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

function contentChanged()
{
	if (target == null)
	{
		target = "content";
	}
	if (xmlhttp.readyState==4)
	{
		document.getElementById(target).innerHTML = xmlhttp.responseText;
	}
}

function headerChanged()
{
	if (xmlhttp2.readyState==4)
	{
		document.getElementById("header").innerHTML = xmlhttp2.responseText;
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
		else if (page == "od")
		{
			args = args + "notes=" + escape(row);
			args = args + "&series=" + escape(od);
			args = args + "&page=" + escape(page);
		}
		else if (page == "oid")
		{
			args = args + "notes=" + escape(row);
			args = args + "&series=" + escape(oid);
			args = args + "&page=" + escape(page);
		}
		
	}
	else
	{
		return "";
	}
	return args;
}
		

function loadContent(divName, pageName)
{	
	target = divName;
	xmlhttp=GetXmlHttpObject();
	if (xmlhttp == null)
	{
		alert ("Your browser does not support XMLHTTP!");
		return;
	} 
	
	var url = pageName;
	url = url + genArgs(pageName);	
	//alert(url);
	xmlhttp.onreadystatechange = contentChanged;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
	
}

function load()
{
    loadContent("content", "main.html");
    row = "A";
}

function callPrime()
{
    //alert("CALLED CALLPRIME!");
	row = document.getElementById("notes").value;
	page = "main";
	//alert(row);
	loadContent('content','primes.cgi');
}

function loadOD()
{
    //alert("CALLED CALLPRIME!");
	alert("Called LoadOD!");
	od = document.getElementById("odseries").value;
	alert("od: " + od);
	page = "od";
	//alert(row);
	loadContent('content','primes.cgi');
}

function loadOID()
{
    //alert("CALLED CALLPRIME!");
	od = document.getElementById("oidseries").value;
	page = "oid";
	//alert(row);
	loadContent('content','primes.cgi');
}

function handleEnter(event, func)
{
	var key = event.keyCode || event.which;
	if (key == 13)
	{
		func();
	}
}