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
	    	 <button type="button" class="btn btn-like" id="add_portfolio_button">Add Portfolio</button>
	    	 <input type="text" id="new_portfolio_name" placeholder="New Portfolio Name...">
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

// This is really a global variable, holding the key representing
// the record currently visible.
var currentKeyToContent;

var TAG_FOR_LIKES = "vote"

function set_html_content(data) {
       $('#content_area').html(decodeURIComponent(data));
}

function set_vote_value(data) {
       $('#vote_quantity').html(decodeURIComponent(data));
}
var global_portfolios = [];
function set_decorations(selector,data,decotype) {
      var names = data;
      var ul = $(selector);
      ul.empty();
      $.each(names, function (idx, elem) {
         ul.append('<span class="mydraggable droppableportfolio">' + elem + "</span>&nbsp;");
         $('.mydraggable').draggable({ revert: true });
         $('.droppableportfolio' ).droppable({
           tolerance: "touch",
           drop: function(event, ui) {
                 var text = $(this).text();
                 $.post("/"+decotype+"/add_record/"+text+"/"+currentKeyToContent
                 ).fail(function() { alert("The addition of that record to that portfolio failed."); });
           }
    });
      })
}

function set_current_key(data) {
     currentKeyToContent = data;
     $.get("/cm-html/"+currentKeyToContent,{ },
         set_html_content
      ).fail(function() { alert("cm-html failed in some way; please try something else."); });
}

function next_handler() {
       $.get("/cm-next/"+currentKeyToContent,{},
           process_record_request
          ).fail(function() { alert("Call to cm-next content manager failed."); });
}

function prev_handler() {
       $.get("/cm-prev/"+currentKeyToContent,{},
           process_record_request
          ).fail(function() { alert("Call to cm-prev content manager failed."); });
}

function like_handler() {
       $.post("/record_integer/"+TAG_FOR_LIKES+"/"+currentKeyToContent+"/"+"1",{},
              set_vote_value
          ).fail(function() { alert("Call to change content manager failed."); });
}

function dislike_handler() {
       $.post("/record_integer/"+TAG_FOR_LIKES+"/"+currentKeyToContent+"/"+"-1",{},
              set_vote_value
          ).fail(function() { alert("Call to change content manager failed."); });
}

function get_portfolio_list() {
       $.get("/portfolio",{},
           function (data) {
                var names = data['data'];
                global_portfolios = names;
                set_decorations('#portfolio_list',names,'portfolio');
           }
          ).fail(function() { alert("Call to portfolio content manager failed."); });
}

function get_tag_list() {
       $.get("/tag",{},
           function (data) { 
                set_decorations('#tag_list',data['data'],'tag');
                global_tags = data['data'];
           }
          ).fail(function() { alert("Call to tag content manager failed."); });
}

function get_current_tag_list(name) {
       $.get("/tag/"+name,{},
           function (data) { 
               datax = jQuery.parseJSON( data );
               set_decorations('#current_tag_list',datax['data'],'tag');
           }
          ).fail(function() { alert("Call to tag content manager failed."); });
}

function get_current_portfolio_list(name) {
       $.get("/portfolio/"+name,{},
           function (data) { 
               datax = jQuery.parseJSON( data );
               set_decorations('#current_portfolio_list',datax['data'],'tag');
           }
          ).fail(function() { alert("Call to portfolio content manager failed."); });
}

function add_portfolio_handler() {
        var name = $('#new_portfolio_name').val();
       $.post("/portfolio/"+name,{},
              get_portfolio_list
          ).fail(function() { alert("Call to change content manager failed."); });
}

function add_tag_handler() {
        var name = $('#new_tag_name').val();
       $.post("/tag/"+name,{},
              get_tag_list
          ).fail(function() { alert("Call to change content manager failed."); });
       $.get("/tag/"+name,{},
           function (data) { set_tags('#current_tag_list',data);}
          ).fail(function() { alert("Call to change content manager failed."); });
}

// BEGIN set up click handlers
$('#next_button').click(next_handler);
$('#prev_button').click(prev_handler);
$('#like_button').click(like_handler);
$('#dislike_button').click(dislike_handler);
$('#add_portfolio_button').click(add_portfolio_handler);
$('#add_tag_button').click(add_tag_handler);
// END   set up click handlers

function isPortfolio(txt) {
    return ($.inArray(txt, global_portfolios) != -1);
}

    $( ".droppablerecord" ).droppable({
           tolerance: "touch",
           drop: function(event, ui) {
                 var text = ui.draggable.text();
                 var portfolio = isPortfolio(text);
                 var key = currentKeyToContent;
                 var deco = (portfolio) ? "portfolio" : "tag";
                 $.post("/"+deco+"/add_record/"+text+"/"+key,
                       function () { process_record_request(key);}
                     ).fail(function() { alert("The addition of that record to the content_area portfolio failed."); });
            }
    });

    $( ".droppablerecord" ).draggable({ revert: true });

    function process_record_request(data) {
       currentKeyToContent = data;
       $.get("/cm-html/"+currentKeyToContent,{ },
           set_html_content
          ).fail(function() { alert("The search failed in some way; please try something else."); });

       $.get("/record_integer/"+TAG_FOR_LIKES+"/"+data,{ },
           set_vote_value
          ).fail(function() { alert("The search failed in some way; please try something else."); });
       get_current_tag_list(currentKeyToContent);
       get_current_portfolio_list(currentKeyToContent);
    }

function get_initial_record() {
   $.get("/cm-useful", { },
           process_record_request
          ).fail(function() { alert("The search failed in some way; please try something else."); });
    }
    
    get_initial_record();

    get_portfolio_list();
    get_tag_list();

  </script>
  </body>
</html>
