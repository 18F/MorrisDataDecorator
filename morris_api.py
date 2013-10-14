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


#BEGIN PORTFOLIO SECTION
@app.route('/portfolio', method='GET')
def read_all_portfolios():
    print "called get portfolio"
# This is ugly....I'm not really sure how to get bottle to return 
# a list as JSON rather than a dictionary
    records = {'data': md.getAllPortfolios()}
    return records

@app.route('/portfolio_export', method='GET')
def export_all_portfolios_as_csv():
    return md.exportPortfoliosCSV()

@app.route('/portfolio_records', method='GET')
def export_all_records_as_csv():
    return md.exportRecordsCSV()


@app.route('/portfolio/<name>', method='GET')
def read_portfolio(name):
    records = md.getPortfolio(name)
    return records

@app.route('/portfolio/<name>', method='POST')
def create_portfolio(name):
    success = str(md.createPortfolio(name))
    return success

@app.route('/portfolio/add_record/<portfolio>/<key>/<record>',method='POST')
def add_record_to_portfolio(key,record,portfolio):
    return md.addRecord(key,record,portfolio)

@app.route('/portfolio/add_record/<portfolio>/<key>/',method='POST')
def add_record_to_portfolio(key,portfolio):
    return md.addRecord(key,"",portfolio)

@app.route('/portfolio/<name>', method='DELETE')
def delete_portfolio( name="Mystery Recipe" ):
    return { "success" : False, "error" : "delete not implemented yet" }
#END PORTFOLIO SECTION


#BEGIN TAG SECTION
@app.route('/tag', method='GET')
def read_all_tags():
    print "called get tag"
# This is ugly....I'm not really sure how to get bottle to return 
# a list as JSON rather than a dictionary
    records = {'data': md.getAllTags()}
    return records

@app.route('/tag_export', method='GET')
def export_all_tags_as_csv():
    return md.exportTagsCSV()

@app.route('/tag_records', method='GET')
def export_all_records_as_csv():
    return md.exportRecordsCSV()

@app.route('/tag/<name>', method='GET')
def read_tag(name):
    records = md.getTag(name)
    return records

@app.route('/tag/<name>', method='POST')
def create_tag(name):
    success = str(md.createTag(name))
    return success

@app.route('/tag/add_record/<tag>/<key>/<record>',method='POST')
def add_record_to_tag(key,record,tag):
    return md.addRecord(key,record,tag)

@app.route('/tag/add_record/<tag>/<key>/',method='POST')
def add_record_to_tag(key,tag):
    return md.addRecord(key,"",tag)

@app.route('/tag/<name>', method='DELETE')
def delete_tag( name="Mystery Recipe" ):
    return { "success" : False, "error" : "delete not implemented yet" }
#END TAG SECTION




@app.route('/record', method='GET')
def get_an_arbitrary_record():
    return { "content" : "This is the first record.  But not really." }

@app.route('/record_integer/<tag>/<key>',method='GET')
def get_record_integer(tag,key):
    return md.getRecordInteger(tag,key)

@app.route('/record_integer/<tag>/<key>/<delta>',method='POST')
def get_record_integer(tag,key,delta):
    return md.changeRecordInteger(tag,key,delta)





