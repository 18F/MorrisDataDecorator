from bottle import Bottle, template,request,TEMPLATE_PATH,static_file,response

import morris_cm

app = Bottle()

# This is a global we want to remain in memory for all persistence 
# across all calls...at least for now.
cm = morris_cm.ExampleMorrisContentManager()

@app.route('/ping_morris_cm_api',method='GET')
def support_ping():
    return "true"

@app.route('/cm/<key>', method='GET')
def get_record(key):
    return cm.keys[key]

@app.route('/cm-html/<key>', method='GET')
def get_html(key):
    return cm.getHTML(key)

@app.route('/cm-next/<key>', method='GET')
def get_next_record(key):
    r = cm.next(key)
    print "cm.next(key) = "+r
    return r

@app.route('/cm-prev/<key>', method='GET')
def get_prev_record(key):
    return cm.prev(key)

@app.route('/cm-useful', method='GET')
def get_useful_record():
    r = cm.getAUsefulKey()
    return r

@app.route('/cm-uploadtext', method='POST')
def upload_text():
    val = request.forms.get('data')
    print "val ="+repr(val)
    r = cm.loadUrlsFromText(val)




