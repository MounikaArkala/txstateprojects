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
	if (xmlhttp.readyState==4)
	{
		document.getElementById("content").innerHTML = xmlhttp.responseText;
	}
}

function headerChanged()
{
	if (xmlhttp2.readyState==4)
	{
		document.getElementById("header").innerHTML = xmlhttp2.responseText;
	}
}

function loadPrimesMain()
{	
	xmlhttp=GetXmlHttpObject();
	if (xmlhttp==null)
	{
		alert ("Your browser does not support XMLHTTP!");
		return;
	} 
	
	var url="loaded.html";
	//url=url+"?q="+str;
	//url=url+"&sid="+Math.random();
	xmlhttp.onreadystatechange = contentChanged;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
	
	url = "header.html";
	xmlhttp2 = GetXmlHttpObject();
	xmlhttp2.onreadystatechange = headerChanged;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}