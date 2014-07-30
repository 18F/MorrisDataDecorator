MorrisDataDecorator
===================

Python web app that let's you upload URLs, tag, collect into portfolios, vote, and export the results as .csv files.

This is part of the PricesPaid (P3) Project
--------------------------------------

The PricesPaid (P3) project is market research tool to allow search of purchase transactions.  It is modularized into 4 github repositories:

1. [PricesPaidGUI](https://github.com/XGov/PricesPaidGUI),
2. [PricesPaidAPI](https://github.com/presidential-innovation-fellows/PricesPaidAPI),
3. [MorrisDataDecorator](https://github.com/presidential-innovation-fellows/MorrisDataDecorator),
4. [P3Auth](https://github.com/XGov/P3Auth).

To learn how to install the system, please refer to the documentation in the PricesPaidGUI project.

The name "PricesPaid" is descriptive: this project shows you prices that have been paid for things.  However, the name is applied to many projects, so "P3" is the specific name of this project.

Introduction
------------

The Morris Data Decorator is a way to decorate objects specified by URL which you don't own.  The objects
can be decorations with integers, such as ratings or votes, can be collected together into portfo
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

This project is currently in a mostly broken state for stand-alone use because I have been using primarily in service to two other projects, PricesPaidGUI and PricesPaidAPI.  However, I would like to restore its stand-alone usage.  It has a nice set of automated user tests which should make this relatively easy.

The code can currently use in memory storage, and SOLR.  The SOLR usage is far more valuable because it is persistent, and represents somethign someone might want to do with stand-alone usage.

However, one could easily implement a file-based, Reddis-based, or SQL-based implementation based on the unit test suites that already exists.

Before I broke it for stand alone use, it used to do this:

As of now, if you install the Morris data decorator and the necessary Python components and then host it,
you will have a GUI that lets you upload a list of URLs.  You can then circle through these URLs, which are
rendered in an IFrame, voting on them, tagging them, and collecting them into portfolios.  You can then
go to the export tab and export your actions via CSV files that you can copy-and-paste.

The easiest way to host it is with Bottle.  With Bottle you can in fact host all of the APIs as well.
You could of course choose to use apache or wsgi if you wanted to, but that will be more work.

It does have several partial test suites that should be of assistance to any would be contributors.

At present it has these limitations:

* Persistence is 100% in memory.  Your site goes down, so does your data.  Think of it
as writing on a napkin, and plan to copy your work from the napkin onto something permanent soon. If you use the SOLR back end, you don't have this problem.
* It doesn't export votes.
* Voting is not handled consistently with the other parts of the API.
* The Iframe usage is pretty ugly.
* The Drag and Drop barely works---you have to drop an item onto the edge of the frame.

In summary, it is a project in very early stage of developement, and opportunities to improve it abound.

Installing
------------------------

This project depends on the python projects:

* Bottle
* requests

I would like to figure out how to package those up, but until I do, just make sure they are both installed.
In fact I have been 7 years away from running open-source projects, and am open to assistance on how
to make this easier to install---please blast me or assist me.

I'm using Python 2.7, but it might work under 3.x.

Here is a basic set of instructions, which are as yet unvetted:
* Install Bottle
* Install requests
* execute: python test_morris.py
* execute: python test_morris_api.py
* exectue: python test_morris_cm.py

If any of the tests fail, you had better email me or figure out why.  Note that to test the API
I am actually spawning Bottle in a thread in order to make a realistic web service call---if the port
is in use, this will fail for that reason.

If you are ready:
* execute: bash run_all.bash
* execute: python run_morris_gui_via_bottle.py

Then point a browser at:
http://localhost:8080

which is being listened to by Bottle.

Go to the Import tab, and past in a list of URLs on separate lines that you would like to
decorate.  This is a particular beautiful set of designs by William Morris which are all from
the freely reusable from wikimedia:

http://upload.wikimedia.org/wikipedia/commons/b/b4/William_Morris_design_for_Trellis_wallpaper_1862.jpg
http://upload.wikimedia.org/wikipedia/commons/3/33/Morris_Windrush_textile_design_1881-83.jpg
http://upload.wikimedia.org/wikipedia/commons/0/0a/Morris_Redcar_carpet_design_c_1881-85.jpg
http://upload.wikimedia.org/wikipedia/commons/8/84/Morris_Bluebell_printed_fabric_design_detail.jpg
http://upload.wikimedia.org/wikipedia/commons/5/5a/Morris_Little_Flower_carpet_design_detail.jpg
http://upload.wikimedia.org/wikipedia/commons/4/44/Morris_Tulip_and_Willow_design_1873.jpg
http://upload.wikimedia.org/wikipedia/commons/c/cf/Morris_Wey_printed_textile_design_c_1883.jpg

Then go to the Decorate tab and start adding portfolios and tags.  You can drag-n-drop the portfolios and
tags onto the content, and the content onto the portfolios and tags.  It doesn't work very smoothly yet.

Then, go to the Export tag, where you will see your data in the form of comma separate value files.  Since
there is no persistence, you should save these files as soon as they are valuable to you, and not rely
on the in-memory persistence.

Why is it called Morris?
------------------------

It is named after one of the greatest decorators of all time, William Morris
http://en.wikipedia.org/wiki/William_Morris.  Morris was a great polymath and
started the "Arts and Crafts" movement in England, amoung other acheivements too numerous to list here.

### Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.

