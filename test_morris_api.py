# I'm going to test through an actual web call, so there is no actuall
# importation of the morris_api file.  Instead, we will rely on Requests.

# You need to have Bottle already running on Port 8080 and answering on
# localhost for these tests to run.

# The set up fixture below starts up the Bottle server on port 8080.
# You could coneivably have a port collision, in which case change the number below.

from bottle import Bottle, run, template,request
import threading

import time
import unittest
import requests
import csv
import StringIO

# We import this to invoke Bottle on it to treat it as a web service,
# but WE DON'T call it directly --- the test_morris.py file does that.
# This file is to test that the Web Service API works.

import morris_api

# By the way, when did API become synonymous with Web Service?  Am I
# the only programmer old enough to remember that we used the term
# Application Programmer Interfaces long before the Internet existed? (sigh.)
# Where did I leave my cane...


BottleHostname = "localhost"
BottlePort = 8080

URLtoMorrisAPI = "http://"+BottleHostname+":"+str(BottlePort);

def runBottleSoWeCanTest():
    run(morris_api.app, host=BottleHostname, port=BottlePort, debug=True,reloader=True)
    return True

class TestMorrisWebServiceAPI(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.bottle_thread = threading.Thread(target=runBottleSoWeCanTest)
        self.bottle_thread.daemon = True
        self.bottle_thread.start()
        # Need to make sure bottle is started up!
        time.sleep(0.3)

    def test_canPingMorrisAPI(self):
        r = requests.get(URLtoMorrisAPI+"/ping_morris_api")
        self.assertTrue(r.status_code == 200)


    def test_canCreatePortfolio(self):
        name = "spud"
        r = requests.post(URLtoMorrisAPI+"/portfolio/"+name)
        self.assertTrue(r.status_code == 200)
        r = requests.get(URLtoMorrisAPI+"/portfolio/"+name)
        self.assertTrue(r.status_code == 200)
        d = r.json()
        print repr(d)

    def add_portfolio(self,name):
        return requests.post(URLtoMorrisAPI+"/portfolio/"+name)

    def add_record(self,name,key,content):
        return requests.post(URLtoMorrisAPI+"/portfolio/add_record/"+name+"/"+key+"/"+content)

    def test_canCreatePortfolioWithRecords(self):
        name = "spud"
        r = self.add_portfolio(name)
        self.assertTrue(r.status_code == 200)
        # now add a record
        key = "mykey"
        content = "mycontent"
        self.add_record(name,key,content)
        r = requests.get(URLtoMorrisAPI+"/portfolio/"+name)
        self.assertTrue(r.status_code == 200)
        d = r.json()
        self.assertTrue(key in d)
        self.assertEqual(d[key],content)

    def test_can_export_portfolios_reports_to_csv(self):
        """"
        We will try to test using a "complete circuit" methodology.
        """
        self.add_portfolio("aaa")
        self.add_record("aaa","r1","c1")
        self.add_record("aaa","r2","c2")
        self.add_portfolio("bbb")
        self.add_record("bbb","r3","c3")
        self.add_record("bbb","r4","c4")
        self.add_portfolio("ccc")
        self.add_record("ccc","r5","c5")
        r = requests.get(URLtoMorrisAPI+"/portfolio_records")
        self.assertTrue(r.status_code == 200)
        # Now we try to build a CSV reader to check that we got what we put in!
        print "r.text = "+r.text
        input = StringIO.StringIO(r.text)
        r = csv.reader(input)
        for row in r:
            print ', '.join(row)

    def test_can_export_portfolio_to_csv(self):
        """"
        We will try to test using a "complete circuit" methodology.
        """
        self.add_portfolio("aaa")
        self.add_portfolio("bbb")
        self.add_portfolio("ccc")
        r = requests.get(URLtoMorrisAPI+"/portfolio_export")
        self.assertTrue(r.status_code == 200)
        print "r.text = "+r.text
        input = StringIO.StringIO(r.text)
        r = csv.reader(input)
        for row in r:
            print ', '.join(row)


# Much more is needed to make this complete---but I am a Spiker!

if __name__ == '__main__':
    unittest.main()
