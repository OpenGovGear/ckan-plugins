<?php?>

<head>
<!--For querying database and dynamically populating web page with query results -->
<script type="text/javascript">

   function ajaxFunction(clicked_id) {
  	var xmlHttp;
  	try
  	{
     	// Firefox, Opera 8.0+, Safari
     	xmlHttp=new XMLHttpRequest();
  	}
  	catch (e)
  	{
     	// Internet Explorer of several flavors
     	try
     	{
        	xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
     	}
     	catch (e)
     	{
        	try
        	{
           	xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
        	}
        	catch (e)
        	{
           	// or nothing works.  Punt.
           	alert("Your browser does not support AJAX!");
           	return false;
        	}
     	}
  	}    

	//create different formats of query string based on whether a date search element
	//or a word search element was pressed
  	if (clicked_id == 'enterPressed' || clicked_id == 'buttonPressed') //word search
  	{    	 
     	  // Create variable names for the form input names and values
     	  // set name to what the user types and url encode it
     	  var word = document.getElementById('enterPressed').value;
     	  if (!word)
     	  {
     	    alert ("Please enter the keyword you would like to search");
     	    return;
     	  }
     	  word = escape(word);
 
     	  var queryString = "category_keywords LIKE '%"+word+"%' ";

  	}
  	else //date search
  	{    	 
     	  // Create variable names for the form input names and values
     	  // set name to what the user types and url encode it
     	  var year = document.getElementById('year').value;
     	  year = escape(year);
 
     	  var month = document.getElementById('month').value;
     	  month = escape(month);

     	  var queryString = "drawing_date LIKE '" + year +"-"+month+"%' ";
  	}

  	// Open the connection and create the URL as a get.  The data will be sent as part of the URL, so it
  	// needs to be appended to the open method call.
  	xmlHttp.open("GET","processAjaxFunction.php?where=" + queryString, true);
 
  	// Send it with no data as the data is sent above as part of the URL.
  	xmlHttp.send(null);

	//When server finishes processing request, use response to populate returnedQuery div
  	xmlHttp.onreadystatechange=function()
  	{
     	if(xmlHttp.readyState==4)
     	{
        	document.getElementById("returnedQuery").innerHTML=xmlHttp.responseText;
     	}
  	}
   }


   $(document).ready
   (
  	function() {document.forms["sqlForm"].submit(); }
   );

   </script>

</head>


<div align="center">

<!--Choose a year for the month of images you want to display -->
<select id="year" name="selectYear" onChange = "ajaxFunction(this.id)">
<option value="2013" selected>2013</option>
<option value="2012">2012</option>
<option value="2011">2011</option>
</select>

<!--Choose a month of images -->
<select id="month" name="selectMonth" onChange = "ajaxFunction(this.id)">
    <!-- <option value="-1">Month:</option> -->
    <option value="01"<?php echo $selectMonth == '01' ? 'selected="selected"' : ''; ?>>Jan</option>
    <option value="02"<?php echo $selectMonth == '02' ? 'selected="selected"' : ''; ?>>Feb</option>
    <option value="03"<?php echo $selectMonth == '03' ? 'selected="selected"' : ''; ?>>Mar</option>
    <option value="04"<?php echo $selectMonth == '04' ? 'selected="selected"' : ''; ?>>Apr</option>
    <option value="05"<?php echo $selectMonth == '05' ? 'selected="selected"' : ''; ?>>May</option>
    <option value="06"<?php echo $selectMonth == '06' ? 'selected="selected"' : ''; ?>>Jun</option>
    <option value="07"<?php echo $selectMonth == '07' ? 'selected="selected"' : ''; ?>>Jul</option>
    <option value="08"<?php echo $selectMonth == '08' ? 'selected="selected"' : ''; ?>>Aug</option>
    <option value="09"<?php echo $selectMonth == '09' ? 'selected="selected"' : ''; ?>>Sep</option>
    <option value="10"<?php echo $selectMonth == '10' ? 'selected="selected"' : ''; ?>>Oct</option>
    <option value="11"<?php echo $selectMonth == '11' ? 'selected="selected"' : ''; ?>>Nov</option>
    <option value="12"<?php echo $selectMonth == '12' ? 'selected="selected"' : ''; ?>>Dec</option>
</select><br>

<!-- text box and button for keyword search -->
<input type="text" id="enterPressed" value="" onkeydown="if (event.keyCode == 13) ajaxFunction(this.id)"/>
<input class="btn btn-small btn-info" name="Keyword Search" id='buttonPressed' value="Keyword Search" type="button" onclick="ajaxFunction(this.id)"/>

</div>

<!-- Create a named space that will be used to put the value returned from the server -->
<br>

<legend></legend>
<br>
<div id="returnedQuery" style="float: center;"></div>

