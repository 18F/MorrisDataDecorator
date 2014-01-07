import morris
import morris_solr
import csv
import sys


SOLR_URL = "http://localhost:8983/solr"
decorator = morris_solr.SolrMorrisDecorator(SOLR_URL)

def import_csv(file,decorator):
    # Read in the csv file
    # Create the portfolios
    # Remove all of the old portfolios


    spamreader = csv.reader(file, delimiter=',', quotechar='"')
    cnt = 0
    for row in spamreader:
        if (cnt != 0 and len(row) == 2):
            print repr(row)
            decoration_id = row[0]
            content = eval(row[1])
            print "Decoration = "+decoration_id + "\n"
            for con in content:
                decorator.associateDecorationWithContentSingle(decoration_id,con)
        cnt = cnt + 1

if __name__ == '__main__':
    import_csv(sys.stdin,decorator)






