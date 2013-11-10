import unittest
import morris
import morris_solr
import test_morris

SOLR_URL = "http://localhost:8983/solr"

class TestMorrisSolrDecorator(test_morris.TestMorrisDecorator):
    def setUp(self):
        self.d = morris_solr.SolrMorrisDecorator(SOLR_URL)
        self.d.deleteAll()

if __name__ == '__main__':
    unittest.main()
