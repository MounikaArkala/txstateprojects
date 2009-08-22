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

function toggleOthers()
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
function getCheckboxList(table)
{
    inputs = table.getElementsByTagName('input');
    var checkboxes = new Array();
    for (i = 0; i < inputs.length; i++)
    {
      if (!inputs[i].length)
      {
        if (inputs[i].type == 'checkbox')
          checkboxes[checkboxes.length] = inputs[i];
      } else
      {
        for(k = 0; k < inputs[i].length; k++)
        {
          if (inputs[i][k].type == 'checkbox')
            checkboxes[checkboxes.length] = inputs[i];
        }
      }
    }
    // checkboxes now is an array of all checkboxes
    // in the table with id "mytablesid".  Now perform some
    // action on the checkboxes.  In this case, check
    // them all.

    return checkboxes;
}
function selectAll()
{
    table = document.getElementById('filtertable');
    checkboxes = getCheckboxList(table);
    for (i = 0; i < checkboxes.length; i++)
    {
      checkboxes[i].checked = true;
    }
}

function selectNone()
{
    table = document.getElementById('filtertable');
    checkboxes = getCheckboxList(table);
    for (i = 0; i < checkboxes.length; i++)
    {
      checkboxes[i].checked = false;
    }
}
function refresh()
{
    document.noteform.submit();
}
