# This file is for using Bottle as your webserver.
from bottle import Bottle, run, template,request

# Because in practice we might have two versions of Bottle 
# running, one for the GUI and one for the API, so by 
# default we will just keep this one here.
import morris_config


import morris_cm_api

# This line is different from app.wsgi---this
# is if you want to run the Bottle webserver itself
# rather than Apache.  I am trying to maintain both,
# in particular because I don't know of a good way to
# implement SSH without Apache
run(morris_cm_api.app, debug=True, reloader=True, port=morris_config.BOTTLE_CONTENT_MANAGER_API_PORT)

