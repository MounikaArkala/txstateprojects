
<html>
<head>
    <title>Object method example 5</title>
</head>
<body>
<?php
class Table {
    var $table_array = array();
    var $headers = array();
    var $cols;
    function Table($headers) {
        $this->headers = $headers;
        $this->cols    = count($headers);
    }
    
    function addRow($row) {
        if (count($row) != $this->cols)
            return false;
        array_push($this->table_array, $row);
        return true;
    }
    
    function rmRow($row) {
        if (count($row) != $this->cols)
            return false;
        // create new array.
        $old_array = $this->table_array;
        $this->table_array = array();
        foreach($old_array as $table_row)
        {
            $add = False;
            $index = 0;
            foreach($row as $item)
            {
                if ($item != $table_row[$index])
                {
                    // found a discrepancy so this row is not match for removal.
                    $add = True;
                }
                $index += 1;
            }
            if ($add) // item should be added to the array (was not a match).
            {
                array_push($this->table_array, $table_row);
            }
        }
        
        return true;
    }
    
    function addRowAssocArray($row_assoc) {
        $row = array();
        foreach($this->headers as $header) {
            if (!isset($row_assoc[$header]))
                $row_assoc[$header] = "";
            $row[] = $row_assoc[$header];
        }
        array_push($this->table_array, $row);
        return true;
    }
    
    
    function rmRowAssocArray($row_assoc) {
        // turn the assoc array into a regular array and then rmRow on it.
        $temp = array();
        foreach($this->headers as $header) {
            if (!isset($row_assoc[$header]))
                $row_assoc[$header] = "";
            $temp[] = $row_assoc[$header];
        }
        $this->rmRow($temp);
        
        return true;
    }
    
    function addCol($colname, $defaultval=null)
    {
        array_push($this->headers, $colname);
        $old_array = $this->table_array;
        $this->table_array = array();
        foreach($old_array as $row)
        {
            array_push($row, $defaultval);
            array_push($this->table_array, $row);
        }
    }
    
    
    
    function output() {
        print "<pre>";
        foreach($this->headers as $header)
            print "<b>$header</b> ";
        print "\n";
        foreach($this->table_array as $y) {
            foreach($y as $xcell)
            {
                if ($xcell === null)
                {
                    $xcell = ' ';
                }
                print "$xcell ";
            }
            print "\n";
        }
        print "</pre>";
    }
}

$test = new table(array("a", "b", "c"));
$test->addRow(array(1,2,3));
$test->addRow(array(5,6,7));
$test->addRowAssocArray(array('b'=>0, 'a'=>6, 'c'=>3));
$test->output();

print "Testing rmRow...<br />";
print "trying to remove a row that doesn't exist (4,3,2) using rmRow:<br />";
$test->rmRow(array(4,3,2));
$test->output();
print "now remove a row that does exist (1,2,3) using rmRow:<br />";
$test->rmRow(array(1,2,3));
$test->output();
print "trying to remove a row that doesn't exist (-1, 2, 0) using rmRowAssocArray:<br />";
$test->rmRowAssocArray(array('b'=>0, 'c'=>2, 'a'=>-1));
$test->output();
print "now removing a row that does exist (5,6,7) using rmRowAssocArray:<br />";
$test->rmRowAssocArray(array('b'=>6, 'a'=>5, 'c'=>7));
$test->output();
print "add a few rows back so we can test our col function...<br />";
$test->addRow(array(1,2,3));
$test->addRow(array(8,3,2));
$test->output();
print "add col w/o specifying default value:<br />";
$test->addCol('h');
$test->output();
print "add col with default value '1':<br />";
$test->addCol('f',1);
$test->output();
?>
</body>
</html>