<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
       <title>Decorate FedBizOps</title>
       <meta name="robots" content="NOINDEX, NOFOLLOW">
    <title>Bootstrap 101 Template</title>
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
           <img class="col-md-8" src="/imgs/William_Morris_design_for_Trellis_wallpaper_1862.jpg" alt="William_Morris_design_for_Trellis_wallpaper_1862">
            </div>
          </div>
          <div class="row">
            <div class="col-md-6" id="control_area">
	    	 <button type="button" class="btn btn-like" id="next_button">Next</button>
		 <button type="button" class="btn btn-dislike" id="prev_button">Prev</button>
            </div>
            <div class="col-md-6">
	    	 <button type="button" class="btn btn-like" id="like_button">Like</button>
                 <span id="vote_quantity"> </span>
		 <button type="button" class="btn btn-dislike" id="dislike_button">Dislike</button>
            </div>
          </div>
          <div class="row" id="portfolios">
            <div class="col-md-6">Portfolios
	    	 <button type="button" class="btn btn-like" id="add_portfolio_button">Add Portfolio</button>
	    	 <input type="text" id="new_portfolio_name" placeholder="New Portfolio Name..."></input>
                 <ul id="portfolio_list"></ul>
            </div>
          </div>
        </div>
        <div class="col-md-4" id="tags">Tags
	    	 <button type="button" class="btn btn-like" id="add_tag_button">Add Tag</button>
	    	 <input type="text" id="new_tag_name" placeholder="New Tag"></input>
                 <ul id="tag_list"></ul>
        </div>
      </div>
  </body>
  <script>

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

function set_portfolios(data) {
      var names = data['data']
      var ul = $('#portfolio_list');
      ul.empty();
      $.each(names, function (idx, elem) {
         ul.append('<div class="mydraggable droppableportfolio">' + elem + "</div>");
         $('.mydraggable').draggable();
         $('.droppableportfolio' ).droppable({
           tolerance: "touch",
           drop: function(event, ui) {
                 var portfolio = $(this).text();
                 alert("mydraggable portfolio = "+portfolio);
                 var key = currentKeyToContent;
                 var record = ""
                 $.post("/portfolio/add_record/"+portfolio+"/"+key+"/"+record
                 ).fail(function() { alert("The addition of that record to that portfolio failed."); });
           }
    });
      })
}


function set_tags(data) {
      var names = data['data']
      var ul = $('#tag_list');
      ul.empty();
      $.each(names, function (idx, elem) {
         ul.append('<div class="mydraggable droppabletag">' + elem + "</div>");
         $('.mydraggable').draggable();
         $('.droppabletag' ).droppable({
           tolerance: "touch",
           drop: function(event, ui) {
                 var portfolio = $(this).text();
                 alert("mydraggable tag = "+tag);
                 var key = currentKeyToContent;
                 var record = ""
                 $.post("/tag/add_record/"+tag+"/"+key+"/"+record
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
           set_portfolios
          ).fail(function() { alert("Call to portfolio content manager failed."); });
}

function get_tag_list() {
       $.get("/tag",{},
           set_tags
          ).fail(function() { alert("Call to tag content manager failed."); });
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
}

// BEGIN set up click handlers
$('#next_button').click(next_handler);
$('#prev_button').click(prev_handler);
$('#like_button').click(like_handler);
$('#dislike_button').click(dislike_handler);
$('#add_portfolio_button').click(add_portfolio_handler);
$('#add_tag_button').click(add_tag_handler);
// END   set up click handlers

    $( ".droppablerecord" ).droppable({
           tolerance: "touch",
           drop: function(event, ui) {
                 var portfolio = ui.draggable.text();
// Is this is a portfolio or a tag?
                 var isPortfolio = true;
                 alert("Content Area portfolio = "+portfolio);
                 var key = currentKeyToContent;
                 var record = ""
                 if (isPortfolio) {
                     $.post("/portfolio/add_record/"+portfolio+"/"+key+"/"+record
                     ).fail(function() { alert("The addition of that record to the content_area portfolio failed."); });
                 } else {
                     $.post("/tag/add_record/"+portfolio+"/"+key+"/"+record
                     ).fail(function() { alert("The addition of that record to the content_area tag failed."); });
                 }
           }
    });

    $( ".droppablerecord" ).draggable();

    function process_record_request(data) {
       currentKeyToContent = data;
       $.get("/cm-html/"+currentKeyToContent,{ },
           set_html_content
          ).fail(function() { alert("The search failed in some way; please try something else."); });

       $.get("/record_integer/"+TAG_FOR_LIKES+"/"+data,{ },
           set_vote_value
          ).fail(function() { alert("The search failed in some way; please try something else."); });
    }

function get_initial_record() {
   $.get("/cm-useful", { },
           process_record_request
          ).fail(function() { alert("The search failed in some way; please try something else."); });
    }
    
    get_initial_record();

    get_portfolio_list();

  </script>

</html>
