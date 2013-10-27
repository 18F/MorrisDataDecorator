from bottle import Bottle, run, template,request,TEMPLATE_PATH,static_file,response

import morris_config 
import requests
import ast
import urllib

app = Bottle()

URL_TO_MORRIS_CM_API = "http://localhost:" + str(morris_config.BOTTLE_CONTENT_MANAGER_API_PORT)
URL_TO_MORRIS_PORTFOLIOS_API = "http://localhost:" + str(morris_config.BOTTLE_DEORATOR_PORTFOLIOS_API_PORT)
URL_TO_MORRIS_TAGS_API = "http://localhost:" + str(morris_config.BOTTLE_DEORATOR_TAGS_API_PORT)
URL_TO_MORRIS_VOTES_API = "http://localhost:" + str(morris_config.BOTTLE_DEORATOR_VOTES_API_PORT)

@app.route('/ping_morris_gui',method='GET')
def trivtest():
    return "true"

@app.route('/js/<filename>')
def server_static(filename):
    return static_file(filename, root="./js/")

@app.route('/', method='GET')
@app.route('/gui-decorate', method='GET')
def present_decorator():
    navbar = template('navbar.tpl')
    return template('decoration_gui.tpl',navbar=navbar)

@app.route('/gui-export', method='GET')
def present_decorator():
    navbar = template('navbar.tpl')
    return template('export.tpl',navbar=navbar)

@app.route('/gui-import', method='GET')
def present_decorator():
    navbar = template('navbar.tpl')
    return template('import.tpl',navbar=navbar)

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

# BEGIN SERVER-SIDE CALLS TO VOTE API
@app.route('/record_integer/<tag>/<key>', method='GET')
def get_record_integer(tag,key):
    r = requests.get(URL_TO_MORRIS_VOTES_API+"/record_integer/"+tag+"/"+key)
    return r.text

@app.route('/record_integer/<tag>/<key>/<delta>', method='POST')
def get_create_record(tag,key,delta):
    r = requests.post(URL_TO_MORRIS_VOTES_API+"/record_integer/"+tag+"/"+key+"/"+delta)
    return r.text
# END SERVER-SIDE CALLS TO VOTE API

# BEGIN SERVER-SIDE CALLS TO MORRIS PORTFOLIO API
@app.route('/portfolio', method='GET')
def get_portfolios():
    r = requests.get(URL_TO_MORRIS_PORTFOLIOS_API+"/decoration")
    d = ast.literal_eval(r.text)
    return d

@app.route('/portfolio/<name>', method='GET')
def get_specific_tags(name):
    r = requests.get(URL_TO_MORRIS_PORTFOLIOS_API+"/content/"+name)
    return r.text

@app.route('/portfolio/<name>', method='POST')
def get_create_portfolio(name):
    r = requests.post(URL_TO_MORRIS_PORTFOLIOS_API+"/decoration/"+name)
    return r.text

@app.route('/portfolio_export', method='GET')
def get_export_portfolio():
    r = requests.get(URL_TO_MORRIS_PORTFOLIOS_API+"/decoration_export")
    return r.text

@app.route('/portfolio_records', method='GET')
def get_records():
    r = requests.get(URL_TO_MORRIS_PORTFOLIOS_API+"/decoration_records")
    return r.text

@app.route('/portfolio_records_with_cd/<columns>', method='GET')
def get_records(columns):
    r = requests.get(URL_TO_MORRIS_PORTFOLIOS_API+"/content_records_with_client_data/"+columns)
    return r.text

@app.route('/portfolio/add_record/<portfolio>/<key>',method='POST')
def add_record_to_portfolio(key,portfolio):
    r = requests.post(URL_TO_MORRIS_PORTFOLIOS_API+"/decoration/add_record/"+portfolio+"/"+key)
    return r.text
# End Portfolio work

# Begin Tag work
@app.route('/tag', method='GET')
def get_tags():
    r = requests.get(URL_TO_MORRIS_TAGS_API+"/decoration")
    d = ast.literal_eval(r.text)
    return d

@app.route('/tag/<name>', method='GET')
def get_specific_tags(name):
    r = requests.get(URL_TO_MORRIS_TAGS_API+"/content/"+name)
    return r.text

@app.route('/tag/<name>', method='POST')
def get_create_tag(name):
    r = requests.post(URL_TO_MORRIS_TAGS_API+"/decoration/"+name)
    return r.text

@app.route('/tag_export', method='GET')
def get_export_tag():
    r = requests.get(URL_TO_MORRIS_TAGS_API+"/decoration_export")
    return r.text

@app.route('/tag_records', method='GET')
def get_records():
    r = requests.get(URL_TO_MORRIS_TAGS_API+"/decoration_records")
    return r.text

@app.route('/tag_records_with_cd/<columns>', method='GET')
def get_records(columns):
    r = requests.get(URL_TO_MORRIS_TAGS_API+"/decoration_records_with_client_data/"+columns)
    return r.text

@app.route('/tag/add_record/<tag>/<key>',method='POST')
def add_record_to_tag(tag,key):
    r = requests.post(URL_TO_MORRIS_TAGS_API+"/decoration/add_record/"+tag+"/"+key)
    return r.text

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

@app.route('/cm-uploadtext', method='POST')
def get_useful_record():
    val = request.forms.get('data')
    requests.post(URL_TO_MORRIS_CM_API+"/cm-uploadtext",{'data' : val})
    # now, we want to add the the urls so uploaded to the client data for
    # the main data itself...
    # this the same computation in morris_cm.py --- this is somewhat 
    # unreliable...this should be placed in morris_cm.py and exposed through
    # the API to be reused here.
    urls = val.split('\n') 
    if "" in urls: urls.remove("")
    i = 0
    for u in urls:
        requests.post(URL_TO_MORRIS_TAGS_API+"/content/add_client_data/"+str(i)+"/url/"+urllib.quote_plus(u))
        requests.post(URL_TO_MORRIS_PORTFOLIOS_API+"/content/add_client_data/"+str(i)+"/url/"+urllib.quote_plus(u))
        requests.post(URL_TO_MORRIS_TAGS_API+"/content/"+str(i))
        requests.post(URL_TO_MORRIS_PORTFOLIOS_API+"/content/"+str(i))
        i = i + 1

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






