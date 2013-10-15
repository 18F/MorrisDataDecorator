<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
       <title>Morris Data Export</title>
       <meta name="robots" content="NOINDEX, NOFOLLOW">
    <title>Export Decorations</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="../../assets/js/html5shiv.js"></script>
      <script src="../../assets/js/respond.min.js"></script>
    <![endif]-->

    <link href="css/decoration_gui.css" rel="stylesheet" media="screen">
  </head>
  <body>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="//code.jquery.com/jquery.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="bootstrap/js/bootstrap.min.js"></script>

  <div class="container">
    {{!navbar}}
    <p>Portfolios:</p>
    <textarea id="export-portfolio-area" class="form-control" rows="5"></textarea>
    <textarea id="export-portfolio-assocations-area" class="form-control" rows="5"></textarea>
    <p>Tags:</p>
    <textarea id="export-tag-area" class="form-control" rows="5"></textarea>
    <textarea id="export-tag-associations-area" class="form-control" rows="5"></textarea>
  </div>
  </body>
  <script>

  $('#export_nav').addClass("active");
  var failMessage = " failed in some way; please try something else.";

   function load_text_area(selector,get_url) {
     function load_text_area(data) {
     	   $(selector).val(data);
     }	   
     function get_data() {
           $.get(get_url, { },
               load_text_area
           ).fail(function() { alert("The search "+get_url+failMessage); });
      }
      get_data();
   }

   load_text_area('#export-portfolio-assocations-area',"/portfolio_records");
   load_text_area('#export-portfolio-area',"/portfolio_export");

   load_text_area('#export-tag-associations-area',"/tag_records");
   load_text_area('#export-tag-area',"/tag_export");
  
 </script>
</html>