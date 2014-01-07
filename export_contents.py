import morris
import morris_solr

SOLR_URL = "http://localhost:8983/solr"

decorator = morris_solr.SolrMorrisDecorator(SOLR_URL)

def export_csv(decorator):
    print decorator.exportDecorationsToContentsAsCSV()

if __name__ == '__main__':
    export_csv(decorator)
