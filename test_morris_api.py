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
import sys

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


    def test_canCreateDecoration(self):
        name = "spud"
        r = requests.post(URLtoMorrisAPI+"/decoration/"+name)
        self.assertTrue(r.status_code == 200)
        r = requests.get(URLtoMorrisAPI+"/decoration/"+name)
        self.assertTrue(r.status_code == 200)


    def add_decoration(self,decoration):
        return requests.post(URLtoMorrisAPI+"/decoration/"+decoration)

    def add_record(self,decoration,content):
        return requests.post(URLtoMorrisAPI+"/decoration/add_record/"+decoration+"/"+content)

    def test_canCreateDecorationWithRecords(self):
        decoration= "spud"
        r = self.add_decoration(decoration)
        self.assertTrue(r.status_code == 200)
        # now add a record
        content = "mykey"
        self.add_record(decoration,content)
        r = requests.get(URLtoMorrisAPI+"/decoration/"+decoration)
        self.assertTrue(r.status_code == 200)
        d = r.json()
        print "d['data']" + repr(d['data'])
        print "XXX"
        print "YYY"
        self.assertTrue(content in d['data'])
        self.assertEqual(d['data'],[content])

    def test_can_export_decorations_reports_to_csv(self):
        """"
        We will try to test using a "complete circuit" methodology.
        """
        self.add_decoration("aaa")
        self.add_record("aaa","r1")
        self.add_record("aaa","r2")
        self.add_decoration("bbb")
        self.add_record("bbb","r3")
        self.add_record("bbb","r4")
        self.add_decoration("ccc")
        self.add_record("ccc","r5")
        r = requests.get(URLtoMorrisAPI+"/decoration_records")
        self.assertTrue(r.status_code == 200)
        # Now we try to build a CSV reader to check that we got what we put in!
        input = StringIO.StringIO(r.text)
        print "r.text = "+r.text
        r = csv.reader(input)
        for row in r:
            print ', '.join(row)

    def test_can_export_decoration_to_csv(self):
        """"
        We will try to test using a "complete circuit" methodology.
        """
        self.add_decoration("aaa")
        self.add_decoration("bbb")
        self.add_decoration("ccc")
        r = requests.get(URLtoMorrisAPI+"/decoration_export")
        self.assertTrue(r.status_code == 200)
        input = StringIO.StringIO(r.text)
        r = csv.reader(input)
        for row in r:
            print ', '.join(row)


# Much more is needed to make this complete---but I am a Spiker!

if __name__ == '__main__':
    unittest.main()
