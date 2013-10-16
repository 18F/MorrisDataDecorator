from bottle import Bottle, template,request,TEMPLATE_PATH,static_file,response

import morris
import StringIO

app = Bottle()

# This is a global we want to remain in memory for all persistence 
# across all calls...at least for now.
md = morris.MorrisDecorator()

@app.route('/ping_morris_api',method='GET')
def trivtest():
    return "true"

#BEGIN DECORATION SECTION
@app.route('/decoration', method='GET')
def read_all_decorations():
    records = {'data': md.getAllDecorations()}
    return records

@app.route('/decoration_export', method='GET')
def export_all_decorations_as_csv():
    return md.exportDecorationsAsCSV()

@app.route('/decoration_records', method='GET')
def export_all_records_as_csv():
    return md.exportDecorationsToContentsAsCSV()

@app.route('/decoration/<name>', method='GET')
def read_decoration(name):
    records = md.getContentsForDecoration(name)
    return {'data': records}

@app.route('/content/<name>', method='GET')
def read_decoration(name):
    records = md.getDecorationsForContent(name)
    return {'data': records}

@app.route('/decoration/<name>', method='POST')
def create_decoration(name):
    success = str(md.createDecorations([name]))
    return success

@app.route('/decoration/add_record/<decoration>/<key>',method='POST')
def add_record_to_decoration(decoration,key):
    return md.associateDecorationWithContentSingle(decoration,key)

@app.route('/decoration/<name>', method='DELETE')
def delete_decoration( name="Mystery Recipe" ):
    return { "success" : False, "error" : "delete not implemented yet" }
#END DECORATION SECTION

#BEGIN MORRIS CONTENT MANAGEMENT
@app.route('/record', method='GET')
def get_an_arbitrary_record():
    return { "content" : "This is the first record.  But not really." }

@app.route('/record_integer/<tag>/<key>',method='GET')
def get_record_integer(tag,key):
    return md.getRecordInteger(tag,key)

@app.route('/record_integer/<tag>/<key>/<delta>',method='POST')
def get_record_integer(tag,key,delta):
    return md.changeRecordInteger(tag,key,delta)
#END MORRIS CONTENT MANAGEMENT





