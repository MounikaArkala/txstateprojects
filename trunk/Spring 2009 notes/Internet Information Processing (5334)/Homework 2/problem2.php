<html>
<head><Title>Problem 2</title></head>
<body>
<br /><br />
<h2>Please submit your query below</h2>
<table>
<form action="problem2.php" method="get">
<tr><td><label for="name">Search by Name: </label></td><td><input name="name" id="name" type="text" /></td>
</form>
<form action="problem2.php" method="get">
<tr><td><label for="dept">Search by Department: </label></td><td><input name="dept" id="dept" type="text" /></td>
</form>
<form action="problem2.php" method="get">
<tr><td><label for="salary">Search by Minimum Salary: </label></td><td><input name="salary" id="salary" type="text" /></td>
</form>
<form action="problem2.php" method="get">
<tr><td><label for="commission">Search by Minimum Commission: </label></td><td><input name="commission" id="commission" type="text" /></td>
</form>
</table>
<?php

print "<br />";
$submission = True;
$output = array();
if (isset($_GET['name']) and strlen($_GET['name']))
{
    $temp = ereg_replace("[^A-Za-z0-9]", "", $_GET['name'] ); // sanitize user input (only allow alpha-numeric items)
    $temp = strtoupper($temp); // capitalize it.
    print "You are searching by name.  Your query was normalized to \"$temp\".<br />";
    exec("export ORACLE_HOME=/opt/oracle/OraHome_1; export TWO_TASK=CSORACLE;./sample2 name %$temp%", &$output);
    // we're doing a 'name' query.
}
else if (isset($_GET['dept']) and strlen($_GET['dept']))
{
    $temp = ereg_replace("[^A-Za-z0-9]", "", $_GET['dept'] ); // sanitize user input (only allow alpha-numeric items)
    $temp = strtoupper($temp); // capitalize it.
    print "You are searching by department.  Your query was normalized to \"$temp\".<br />";
    exec("export ORACLE_HOME=/opt/oracle/OraHome_1; export TWO_TASK=CSORACLE;./sample2 dept %$temp%", &$output);
}
else if (isset($_GET['salary']) and strlen($_GET['salary']))
{
    $temp = ereg_replace("[^0-9]", "", $_GET['salary']); // sanitize user input (only allow numeric items)
    print "You are searching by minimum salary.  Your query was normalized to \"$temp\".<br />";
    exec("export ORACLE_HOME=/opt/oracle/OraHome_1; export TWO_TASK=CSORACLE;./sample2 salary $temp", &$output);
}
else if (isset($_GET['commission']) and strlen($_GET['commission']))
{
    $temp = ereg_replace("[^0-9]", "", $_GET['commission']); // sanitize user input (only allow numeric items)
    print "You are searching by commission.  Your query was normalized to \"$temp\".<br />";
    exec("export ORACLE_HOME=/opt/oracle/OraHome_1; export TWO_TASK=CSORACLE;./sample2 commission $temp", &$output);
}
else
{
    // they didn't submit anything.
    $submission = False;
}

if ($submission)
{
    // print our output table.
    if (count($output) == 0)
    {    
        print "<h2>Your query returned no results!</h2>";
    }
    else
    {
        print "<br />";
        print "<table>";
        print "<tr><th>Employee Name</th><th>Salary</th><th>Commission</th></tr>";
        foreach($output as $o)
        {
            print "<tr>";
            foreach(preg_split("/\s+|,/", $o) as $td)
            {
                print "<td>$td</td>";
            }
            print "</tr>";
        }
        print "</table>";
    }
}

?>
</body>
</html>