MorrisDataDecorator
===================

Python web app that let's you upload URLs, tag, collect into portfolios, vote, and export the results as .csv files.

This project depends up:

Bottle
requests
ast (Possibly this is a builtin?)

I would like to figure out how to package those up, but until I do, just make sure they are both installed.


Introduction
------------

The Morris Data Decorator is a way to decorate objects specified by URL which you don't own.  The objects
can be decorations with integers, such as ratings or votes, can be collected together into portfolios or 
subsets, and can be tagged with strings, or tag clouds.

It provides a simple GUI which operates against 3 distinct APIs: one for content management, one for tags,
and one for portfolios.  However, since the nature of "decoration" is so general, just being an association
of strings to the content managed (such as urls), one can easily imagine a different GUI that use more or 
fewer instances.  The project really consists of both APIs, and the GUI which uses them, and a given 
reuser of the code might want to use only one piece or the other.

This was created in two weeks as a side project for me to learn about drag-and-drop and to create an API-based
way fo storing portfolios and tags.  My hope is that that project (the Prices Paid project) will utilize this 
one eventually.


Status
------

As of now, if you install the Morris data decorator and the necessary Python components and then host it, 
you will have a GUI that lets you upload a list of URLs.  You can then circle through these URLs, which are 
rendered in an IFrame, voting on them, tagging them, and collecting them into portfolios.  You can then 
go to the export tab and export your actions via CSV files that you can copy-and-paste.

The easiest way to host it is with Bottle.  With Bottle you can in fact host all of the APIs as well.
You could of course choose to use apache or wsgi if you wanted to, but that will be more work.

It does have several partial test suites that should be of assistance to any would be contributors.

At present it has these limitations:

* Persistence is 100% in memory.  Your site goes down, so does your data.  Think of it 
as writing on a napkin, and plan to copy your work from the napkin onto something permanent soon.
* It doesn't export votes.
* Voting is not handled consistently with the other parts of the API.
* The Iframe usage is pretty ugly.
* The Drag and Drop barely works---you have to drop an item onto the edge of the frame.

In summary, it is a project in very early stage of developement, and opportunities to improve it abound.


Why is it called Morris?
------------------------

It is named after one of the greatest decorators of all time, William Morris 
http://en.wikipedia.org/wiki/William_Morris.  Morris was a great polymath and 
started the "Arts and Crafts" movement in England, amoung other acheivements too numerous to list here.





