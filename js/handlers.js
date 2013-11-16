// I don't understand how to manage namespaces correctly in javascript.

// I have broken this out as a separate file because the GUI (HTML)
// is highy variable by project.  In particular, I am now trying 
// to use this from the PricesPaidGUI, which clearly cannot use this 
// same GUI.  However, each of the individual HTML components can
// more or less be reused.


// This is really a global variable, holding the key representing
// the record currently visible.

var HANDLER_NAMESPACE_OBJECT = {
    portfolo_url : "/portfolio",
    tag_url : "/tag",
    refresh_droppables : function() {}
}

var currentKeyToContent;

var TAG_FOR_LIKES = "vote"

function set_html_content(data) {
       $('#content_area').html(
          '<iframe height="400" width="600" src="'+decodeURIComponent(data)+'"/>'
        );
}

function set_vote_value(data) {
       $('#vote_quantity').html(decodeURIComponent(data));
}
var global_portfolios = [];
function set_decorations(url,selector,data) {
      var names = data;
      var ul = $(selector);
      ul.empty();
      $.each(names, function (idx, elem) {
	  var name = elem;
	  var close_id = ' id="draggable-close-'+name+'"';
	  var draggable_id = ' id="draggable-id-'+name+'"';
// TODO: This won't handle spaces, we probably need a javascript URL-encode here,
// which means we will have to be very careful to unencode below
          ul.append('<div '+draggable_id+' style="z-index: 1" class="decoration mydraggable droppableportfolio"><img class="draggable-handle" src="./MorrisDataDecorator/imgs/icn_list.svg" alt="drag">' + 
'<span class="draggable-name">' + 
elem  + 
'</span>' + 
'<img class="draggable-close" '+close_id+' src="./MorrisDataDecorator/imgs/gnome_window_close.png" alt="delete">&nbsp;' +
'</div>'
);
         $('.mydraggable').draggable({ revert: true });
         $('.droppableportfolio' ).droppable({
           tolerance: "touch",
           drop: function(event, ui) {
               var text = $(this).attr('id').substring("draggable-id-".length);
                 $.post(url+"/add_record/"+text+"/"+currentKeyToContent
                 ).fail(function() { alert("The addition of that record to that portfolio failed."); });
           }
	 });
      $('#draggable-close-'+name).click(
	     function(event) {
                 var text = $(this).attr('id').substring("draggable-close-".length);
                 $.post(url+"/delete_decoration/"+text
                       ).fail(function() 
			      { alert("The deletion of that decoration failed."+text+"|"+decotype); });
// We really need to stop event bubbling on this, this line should do it.
		 event.stopPropagation ? event.stopPropagation() : (event.cancelBubble=true);   
// Now we need to refresh the portfolio_list, or some list...
	  // we probably need to pass this in as a function...
		 get_portfolio_list();

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

function get_portfolio_list(finish_func) {
    $.get(HANDLER_NAMESPACE_OBJECT.portfolio_url,{},
           function (data) {
                var names = data['data'];
                global_portfolios = names;
               set_decorations(HANDLER_NAMESPACE_OBJECT.portfolio_url,
'#portfolio_list',names);
//	       HANDLER_NAMESPACE_OBJECT.refresh_droppables();
	       finish_func();
           }
          ).fail(function() { alert("Call to portfolio content manager failed."); });
}

function get_tag_list(finish_func) {
    $.get(HANDLER_NAMESPACE_OBJECT.tag_url,{},
           function (data) { 
	       alert("tags"+data['data']);
               set_decorations(HANDLER_NAMESPACE_OBJECT.tag_url,'#tag_list',data['data']);
                global_tags = data['data'];
	       finish_func();
           }
          ).fail(function() { alert("Call to tag content manager failed."); });
}

function get_current_tag_list(name) {
       $.get(HANDLER_NAMESPACE_OBJECT.tag_url+"/"+name,{},
           function (data) { 
               datax = jQuery.parseJSON( data );
               set_decorations(HANDLER_NAMESPACE_OBJECT.tag_url,'#current_tag_list',datax['data']);
           }
          ).fail(function() { alert("Call to tag content manager failed."); });
}

function get_current_portfolio_list(name) {
       $.get(HANDLER_NAMESPACE_OBJECT.portfolio_url+"/"+name,{},
           function (data) { 
               datax = jQuery.parseJSON( data );
               set_decorations(HANDLER_NAMESPACE_OBJECT.portfolio_url,'#current_portfolio_list',datax['data']);
           }
          ).fail(function() { alert("Call to portfolio content manager failed for:"+name); });
}

function add_portfolio_handler() {
        var name = $('#new_portfolio_name').val();
       $.post(HANDLER_NAMESPACE_OBJECT.portfolio_url+"/"+name,{},
              function() { get_portfolio_list(); }
          ).fail(function() { alert("Call to change content manager failed."); });
}

function add_tag_handler() {
        var name = $('#new_tag_name').val();
       $.post(HANDLER_NAMESPACE_OBJECT.tag_url + "/"+name,{},
              get_tag_list
          ).fail(function() { alert("Call to change content manager failed."); });
       $.get(HANDLER_NAMESPACE_OBJECT.tag_url + "/"+name,{},
           function (data) { set_tags('#current_tag_list',data);}
          ).fail(function() { alert("Call to change content manager failed."); });
}


function isPortfolio(txt) {
    return ($.inArray(txt, global_portfolios) != -1);
}


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
    

