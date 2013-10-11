# This file is for using Bottle as your webserver.
from bottle import Bottle, run, template,request


import morris_gui

run(morris_gui.app,  debug=True,reloader=True)

