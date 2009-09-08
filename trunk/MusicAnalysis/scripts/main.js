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


/**
* getElementsByClassName()
* Written by Jonathan Snook, http://www.snook.ca/jonathan
* Add-ons by Robert Nyman, http://www.robertnyman.com
*/

function getElementsByClassName(oElm, strTagName, strClassName){
  var arrElements = (strTagName == "*" && oElm.all)? oElm.all : oElm.getElementsByTagName(strTagName);
  var arrReturnElements = new Array();
  strClassName = strClassName.replace(/\-/g, "\\-");
  var oRegExp = new RegExp("(^|\\s)" + strClassName + "(\\s|$)");
  var oElement;
  for (var i = 0; i < arrElements.length; i++) {
    oElement = arrElements[i];
    if (oRegExp.test(oElement.className)) {
      arrReturnElements.push(oElement);
    }
  }
  return (arrReturnElements);
}


/*
===============================
=   MusicAnalysis Functions   =
===============================
*/


function handleEnter(event, func)
{
    /*
    Purpose: a very simple wrapper that will call a function if
    event's key is the same as the keyboard "enter" button.  */
	var key = event.keyCode || event.which;
	if (key == 13)
	{
		return func();
	}
}



