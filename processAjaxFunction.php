<html><head><title>Lab 9 - MySQL and Ajax</title></head>
<body>
<?php
// Get input from HTML
// $select = ($_GET['select']);
// $from = ($_GET['from']);

error_reporting(0);

// Include MySQL class
require_once('../../inc/mysql.class.php');

// Connect to the MySQL server.
//include ("../../database_connection.php");
require_once("../../inc/global.inc.php");

// Die if cannot connect
 if (!$LinkID) {
die('Could not connect: ' . mysql_error());
 }

//Choose the DB and run a query.
 mysql_select_db("moiracarlson199", $LinkID);

//run the query

//$query = "select image_file_name, DATE_FORMAT(drawing_date, '%M %e, %Y' ) from products where drawing_date like '$select-$from%' ";
$queryWhere =  ($_GET['where']);
$query = "select image_file_name, DATE_FORMAT(drawing_date, '%M %e, %Y' ) from products where ".$queryWhere;
 $result = mysql_query( "$query" ,$LinkID);
?>

 <p>

<?php
// Reset the result pointer and display again in a table with titles.
 mysql_data_seek ($result, 0);

//add query results to separate arrays
$resultIMGS = array();
$resultDates = array();
if ($result){
  while($r=mysql_fetch_row($result)) {
  	$resultIMGS[] = $r[0];
  	$resultDates[] = $r[1];
    
  }
}

 print "<table border='0'>";
$maxPerRow =6;
$imgStartInterval = 7;
$dateStartInterval = 7;

	while ( current($resultIMGS) != false ){
  	print "<tr>";
 	 
  	$currentIMG = current($resultIMGS);
  				   
     while ( ($imgStartInterval++ % $maxPerRow != 0) && ($currentIMG != false) )  {
   	 
      	print "<td>";
      	print "<a href='closeUp.php?imageName=$currentIMG'>";
      	print "<img border='0' src='images/{$currentIMG}_small.bmp'>";
      	print "</td>";      		 
      	$currentIMG = next($resultIMGS);
      }
    
    
	print "</center></tr><center><tr>";
    
    $currentDate = current($resultDates);    
      
   	while ( ($dateStartInterval++ % $maxPerRow != 0) && ($currentDate != false) ) {
      	    
      	print "<td>";
      	print "<p align='center'><font face='Arial' size='1'>$currentDate</font></p>";    	 
      	print "</td>";        	 
      	$currentDate = next($resultDates);
      }
    
	print"</tr>";
 
	}

print "</table>";
?>
</body>
</html>

