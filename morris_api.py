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

@app.route('/portfolio/<name>', method='DELETE')
def delete_portfolio( name="Mystery Recipe" ):
    return { "success" : False, "error" : "delete not implemented yet" }

@app.route('/record', method='GET')
def get_an_arbitrary_record():
    return { "content" : "This is the first record.  But not really." }

@app.route('/record_integer/<tag>/<key>',method='GET')
def get_record_integer(tag,key):
    return md.getRecordInteger(tag,key)

@app.route('/record_integer/<tag>/<key>/<delta>',method='POST')
def get_record_integer(tag,key,delta):
    return md.changeRecordInteger(tag,key,delta)





