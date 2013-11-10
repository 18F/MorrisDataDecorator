from bottle import Bottle, template,request,TEMPLATE_PATH,static_file,response

import morris
import morris_memory
import morris_solr
import StringIO
import sys
import logging

logger = logging.getLogger('morris_api_logger')
hdlr = logging.FileHandler('../logs/morris_api.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

app = Bottle()

# This is a global we want to remain in memory for all persistence 
# across all calls...at least for now.
# md = morris_memory.InMemoryMorrisDecorator()

SOLR_URL = "http://localhost:8983/solr"

md = morris_solr.SolrMorrisDecorator(SOLR_URL)

@app.route('/ping_morris_api',method='GET')
def trivtest():
    return "true"

# Obviously, this should be used cautiously.
# It exists mainly to support testing through the API.
@app.route('/delete_all',method='GET')
def delete_all():
    md.deleteAll()


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

@app.route('/decoration_records_with_client_data/<columns>', method='GET')
def export_all_records_as_csv_with_client_data(columns):
    cols = columns.split(',')
    return md.exportDecorationsToContentsAsCSVWithClientDataColumns(cols)

@app.route('/content_records_with_client_data/<columns>', method='GET')
def export_all_records_as_csv_with_client_data(columns):
    cols = columns.split(',')
    return md.exportContentsToDecorationsAsCSVWithClientDataColumns(cols)

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

@app.route('/content/<name>', method='POST')
def create_content(name):
    success = str(md.createContents([name]))
    return success

@app.route('/decoration/add_client_data/<decoration>/<data_name>/<cd:path>', method='POST')
def add_client_data_decoration(decoration,data_name,cd):
    md.addClientDataDecoration(decoration,data_name,cd)
    return {}

@app.route('/content/add_client_data/<content>/<data_name>/<cd:path>', method='POST')
def add_client_data_content(content,data_name,cd):
    md.addClientDataContent(content,data_name,cd)
    return {}

@app.route('/test/add_client_data/<content>/<data_name>/<cd:path>', method='POST')
def test_content(content,data_name,cd):
    md.addClientDataContent(content,data_name,"spud")
    return {}

@app.route('/decoration/add_record/<decoration>/<key>',method='POST')
def add_record_to_decoration(decoration,key):
    logger.info("Called add_record_to_decoration({0},{1})".format(decoration,key))
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






