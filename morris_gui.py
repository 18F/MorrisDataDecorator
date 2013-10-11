from bottle import Bottle, run, template,request,TEMPLATE_PATH,static_file,response

import morris_config 
import requests
import ast

app = Bottle()

URL_TO_MORRIS_API = "http://localhost:" + str(morris_config.BOTTLE_DEORATOR_API_PORT)

URL_TO_MORRIS_CM_API = "http://localhost:" + str(morris_config.BOTTLE_CONTENT_MANAGER_API_PORT)

@app.route('/ping_morris_gui',method='GET')
def trivtest():
    return "true"

@app.route('/', method='GET')
@app.route('/gui-decorate', method='GET')
def present_decorator():
    navbar = template('navbar.tpl')
    return template('decoration_gui.tpl',navbar=navbar)

@app.route('/gui-export', method='GET')
def present_decorator():
    navbar = template('navbar.tpl')
    return template('export.tpl',navbar=navbar)

def pass_through_to_api(r):
    # This is inefficient, but I can't seem to get Bottle to
    # let me procure a correct JSON response with out using a dictionary.
    # I tried using BaseResponse.  This could be my weakness
    # with Python or confusion in Bottle.
    d = ast.literal_eval(r.text)
    return d

# perhaps the morris_api functionality should be presentable by pjson...
# but given the editability we are trying to support, I feel like that might 
# be too much.

# BEGIN SERVER-SIDE CALLS for Morris Decorator
@app.route('/record_integer/<tag>/<key>', method='GET')
def get_record_integer(tag,key):
    r = requests.get(URL_TO_MORRIS_API+"/record_integer/"+tag+"/"+key)
    return r.text

@app.route('/record_integer/<tag>/<key>/<delta>', method='POST')
def get_create_record(tag,key,delta):
    r = requests.post(URL_TO_MORRIS_API+"/record_integer/"+tag+"/"+key+"/"+delta)
    return r.text

@app.route('/portfolio', method='GET')
def get_portfolios():
    r = requests.get(URL_TO_MORRIS_API+"/portfolio")
    d = ast.literal_eval(r.text)
    print "d = "+repr(d)
    return d

@app.route('/portfolio/<name>', method='POST')
def get_create_portfolio(name):
    print "Calling to post portfolio"
    r = requests.post(URL_TO_MORRIS_API+"/portfolio/"+name)
    return r.text

@app.route('/portfolio_export', method='GET')
def get_export_portfolio():
    r = requests.get(URL_TO_MORRIS_API+"/portfolio_export")
    return r.text

@app.route('/portfolio_records', method='GET')
def get_records():
    r = requests.get(URL_TO_MORRIS_API+"/portfolio_records")
    return r.text

@app.route('/portfolio/add_record/<portfolio>/<key>/<record>',method='POST')
def add_record_to_portfolio(key,record,portfolio):
    r = requests.post(URL_TO_MORRIS_API+"/portfolio/add_record/"+portfolio+"/"+key+"/"+record)
    return r.text
# END SERVER-SIDE CALLS for Morris Content Manager


# BEGIN SERVER-SIDE CALLS for Morris Content Manager
@app.route('/cm/<key>', method='GET')
def get_record(key):
    r = requests.get(URL_TO_MORRIS_CM_API+"/cm/"+key)
    return pass_through_to_api(r)

@app.route('/cm-html/<key>', method='GET')
def get_html(key):
    return requests.get(URL_TO_MORRIS_CM_API+"/cm-html/"+key).text

@app.route('/cm-next/<key>', method='GET')
def get_next_record(key):
    return requests.get(URL_TO_MORRIS_CM_API+"/cm-next/"+key).text

@app.route('/cm-prev/<key>', method='GET')
def get_prev_record(key):
    return requests.get(URL_TO_MORRIS_CM_API+"/cm-prev/"+key).text

@app.route('/cm-useful', method='GET')
def get_useful_record():
    return requests.get(URL_TO_MORRIS_CM_API+"/cm-useful").text

# END SERVER-SIDE CALLS for Morris Content Manager

@app.route('/bootstrap/css/<path:path>')
def css_static(path):
    return static_file(path, root="./bootstrap/css/")

@app.route('/bootstrap/js/<filename>')
def js_static(filename):
    return static_file(filename, root="./bootstrap/js/")

@app.route('/css/<path:path>')
def css_static(path):
    return static_file(path, root="./css/")

@app.route('/imgs/<filename>')
def js_static(filename):
    return static_file(filename, root="./imgs/")





