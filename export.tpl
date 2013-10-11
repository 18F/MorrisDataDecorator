<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
       <title>Decorate FedBizOps</title>
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
    <textarea id="export-portfolio-area" class="form-control" rows="3"></textarea>
    <textarea id="export-records-area" class="form-control" rows="3"></textarea>
  </div>
  </body>
  <script>

  function load_portfolio_area(data) {
  	   $('#export-portfolio-area').val(data);
  }

  function get_portfolios() {
      $.get("/portfolio_export", { },
           load_portfolio_area
          ).fail(function() { alert("The search failed in some way; please try something else."); });
   }
    
   get_portfolios();

  function load_records_area(data) {
  	   alert("data"+data)
  	   $('#export-records-area').val(data);
  }

  function get_records() {
      $.get("/portfolio_records", { },
           load_records_area
          ).fail(function() { alert("The search failed in some way; please try something else."); });
   }
    
   get_records();
  
 </script>
</html>