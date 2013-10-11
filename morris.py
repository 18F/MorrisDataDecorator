# Morris is a decorator system for decorating objects that may not be under full control of the 
# implementor of the Morris system.  Decorations including scoring, tagging, and creating portfolios.


class MorrisDecorator:
    """Morris is a decorator system for decorating objects that may not be under full control of the 
implementer of the Morris system.  Decorations including scoring, tagging, and creating portfolios.
"""
    def __init__(self):
        self.portfolios = {}
        # This is a dictionaries of dictionaries.
        # The first dictionary maps "tags" to dictionaries wich map records to integers.
        self.integerTagMaps = {}

    def createPortfolio(self,name):
        p = {}
        self.portfolios[name] = p
        return True
    def getAllPortfolios(self):
        return self.portfolios.keys()

    def getPortfolio(self,name):
        return self.portfolios[name]

    def addRecord(self,key,record,portfolio):
        p = self.getPortfolio(portfolio)
        p[key] = record
        print "added key ="+key
        return p

    def delRecord(self,record_key,portfolio):
        p = self.getPortfolio(portfolio)
        if (record_key in p):
            del p[record_key]
            return True
        else:
            return False

    def getAllPortfoliosContainingRecord(record):
        return True

    def getRecordInteger(self,tag,recordkey):
        if (tag in self.integerTagMaps):
            m = self.integerTagMaps[tag]
            if (recordkey in m):
                return str(m[recordkey])
            else:
                return str(0)
        else:
            return str(0)

    def changeRecordInteger(self,tag,recordkey,delta):
        if (tag not in self.integerTagMaps):
            self.integerTagMaps[tag] = {}
        m = self.integerTagMaps[tag]
        if (recordkey in m):
            m[recordkey] = m[recordkey] + int(delta)
        else:
            m[recordkey] = int(delta)
        return str(m[recordkey])


    def exportPortfoliosCSV(self):
        """
    Export the entire datastore as a CSV file
        """
        retval = ""
        # I'm pretty sure this is terribly inefficent...
        # there must be a better way to do this in python.
        retval = retval + "Portfolio\n"
        for p in self.portfolios.keys():
            retval = retval + p + "\n"
        return retval

    def exportRecordsCSV(self):
        """
    Export the entire datastore as a CSV file
        """
        retval = ""
        # I'm pretty sure this is terribly inefficent...
        # there must be a better way to do this in python.
        retval = retval + "Portfolio,Record,Data\n"
        for p in self.portfolios.keys():
            pf = self.portfolios[p]
            for r in pf.keys():
                retval = retval + p + "," + r + "," + pf[r] + "\n"

        print "exporting retval = "+retval
        return retval


        
