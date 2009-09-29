/* Scales.js
------------------------------
Author:    Luke Paireepinart
Copyright: Nico Schüler

Texas State University
Summer 2009
------------------------------
Brief Summary:
A few routines for error-checking and getting the correct values set up for passing to the
back-end Python script.
*/


function testSubmit()
{
    // perform simple error-checking before submitting.
    
    // Grab the current value of the search field.
	row = document.getElementById("notes").value;
    row = row.trim();
    // Do some error-checking.
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
    return true;
}

function disableWrapCheckbox()
{
    if (document.noteform.order.checked)
    {
        document.noteform.wrap.disabled = false;
    }
    else
    { 
        //document.noteform.wrap.checked = false;
        document.noteform.wrap.disabled = true;
    }
    
}

function load()
{
    formDefaultValues();
    disableWrapCheckbox();
    return true;
}


/**
* Code below written by Rob Schmitt of The Web Developer's Blog
* http://webdeveloper.beforeseven.com/
*/

/**
* The following variables may be adjusted
*/
var active_color = '#000'; // Colour of user provided text
var inactive_color = '#999'; // Colour of default text

/**
* No need to modify anything below this line
*/
window.onload = formDefaultValues;

function formDefaultValues() {
  var fields = getElementsByClassName(document, "input", "default-value");
  if (!fields) {
    return;
  }
  var default_values = new Array();
  for (var i = 0; i < fields.length; i++) {
    fields[i].style.color = inactive_color;
    if (!default_values[fields[i].id]) {
      default_values[fields[i].id] = fields[i].value;
    }
    fields[i].onfocus = function() {
      if (this.value == default_values[this.id]) {
        this.value = '';
        this.style.color = active_color;
      }
      this.onblur = function() {
        if (this.value == '') {
          this.style.color = inactive_color;
          this.value = default_values[this.id];
        }
      }
    }
  }
}
