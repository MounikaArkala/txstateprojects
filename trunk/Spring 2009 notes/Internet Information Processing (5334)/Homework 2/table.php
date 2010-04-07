
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
    
    function output() {
        print "<pre>";
        foreach($this->headers as $header)
            print "<b>$header</b> ";
        print "\n";
        foreach($this->table_array as $y) {
            foreach($y as $xcell)
                print "$xcell ";
            print "\n";
        }
        print "</pre>";
    }
}

$test = new table(array("a", "b", "c"));
$test->addRow(array(1,2,3));
$test->addRow(array(5,6,7));
$test->addRowAssocArray(array(b=>0, a=>6, c=>3));
$test->output();
?>
</body>
</html>