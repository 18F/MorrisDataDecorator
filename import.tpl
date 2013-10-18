<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
       <title>Morris Data Import</title>
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
    <p>
      <button type="button" class="btn btn-like" id="upload_text">Upload Text</button>
Paste URLs to be decorated: </p> 
    <textarea id="import-url-area" class="form-control" rows="50"></textarea>
  </div>
  </body>
  <script>

  $('#import_nav').addClass("active");

  $('#upload_text').click(upload_text_area);

  function upload_text_area() {
     var text = $('#import-url-area').val();
     alert("text = "+text);
            $.post("/cm-uploadtext",
	       { 'data': text}
	    ).fail(function() 
	       { alert("Call to upload content manager failed."); });
  }

 </script>
</html>