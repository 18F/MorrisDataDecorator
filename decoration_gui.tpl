<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
       <title>Morris Data Decorator</title>
       <meta name="robots" content="NOINDEX, NOFOLLOW">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="../../assets/js/html5shiv.js"></script>
      <script src="../../assets/js/respond.min.js"></script>
    <![endif]-->
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="//code.jquery.com/jquery.js"></script>


     <!-- Here I am including JQuery UI, mainly for the Drag n Drop -->
    <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
  <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>

    <link href="css/decoration_gui.css" rel="stylesheet" media="screen">


    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="bootstrap/js/bootstrap.min.js"></script>

<style>
  #draggable { width: 100px; height: 100px; padding: 0.5em; float: left; margin: 10px 10px 10px 0; }
  #droppable { width: 150px; height: 150px; padding: 0.5em; float: left; margin: 10px; }
  </style>

  </head>
  <body>


  <div class="container">
    {{!navbar}}
      <div class="row">
        <div class="col-md-8" >
          <div class="row">
            <div class="col-md-8 droppablerecord" id="content_area">
            </div>
          </div>
          <div class="row">
            <div class="col-md-4" id="control_area">
	    	 <button type="button" class="btn btn-like" id="next_button">Next</button>
		 <button type="button" class="btn btn-dislike" id="prev_button">Prev</button>
            </div>
            <div class="col-md-4">
	    	 <button type="button" class="btn btn-like" id="like_button">Like</button>
                 <span id="vote_quantity"> </span>
		 <button type="button" class="btn btn-dislike" id="dislike_button">Dislike</button>
            </div>
          </div>
          <div class="row">
            <div class="col-md-4" id="current_decorations">
                <p>Tags For This Record</p>
                 <ul id="current_tag_list"></ul>
            </div>
            <div class="col-md-4">
                <p>Portfolios For This Record</p>
                 <ul id="current_portfolio_list"></ul>
            </div>
          </div>
          <div class="row" id="portfolios">
            <div class="col-md-8"> 
	    	 <input type="text" id="new_portfolio_name" placeholder="New Portfolio Name...">
	    	 <button type="button" class="btn btn-like" id="add_portfolio_button">Create Portfolio</button>
               <div>All Portfolios</div>
                 <ul id="portfolio_list"></ul>
            </div>
          </div>
        </div>
        <div class="col-md-4" id="tags">
	    	 <button type="button" class="btn btn-like" id="add_tag_button">Add Tag</button>
	    	 <input type="text" id="new_tag_name" placeholder="New Tag...">
                 <p>All Tags</p>
                 <ul id="tag_list"></ul>
        </div>

        </div>
      </div>

  <script>
  $('#decorate_nav').addClass("active");
  </script>

<script src="js/handlers.js"></script>>

<script>

var portfolio_url = "/portfolio";
var tag_url = "/tag";

HANDLER_NAMESPACE_OBJECT.portfolio_url = portfolio_url;
HANDLER_NAMESPACE_OBJECT.tag_url = tag_url;

// BEGIN set up click handlers
$('#next_button').click(next_handler);
$('#prev_button').click(prev_handler);
$('#like_button').click(like_handler);
$('#dislike_button').click(dislike_handler);
$('#add_portfolio_button').click(add_portfolio_handler);
$('#add_tag_button').click(add_tag_handler);
// END   set up click handlers

    get_initial_record();
    get_portfolio_list();
    get_tag_list();

    $( ".droppablerecord" ).droppable({
           tolerance: "touch",
           drop: function(event, ui) {
                 var text = ui.draggable.text();
                 var portfolio = isPortfolio(text);
                 var key = currentKeyToContent;
                 var deco = (portfolio) ? HANDLER_NAMESPACE_OBJECT.portfolio_url
		                        : HANDLER_NAMESPACE_OBJECT.tag_url;
                 $.post(deco+"/add_record/"+text+"/"+key,
			function () { process_record_request(key);}
                     ).fail(function() { alert("The addition of that record to the content_area portfolio failed."); });
            }
	});

    $( ".droppablerecord" ).draggable({ revert: true });

</script>
  </body>
</html>
