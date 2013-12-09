from abc import ABCMeta,abstractproperty
from morris import AbstractMorrisDecorator
import solr
import sys
import urllib
import datetime
import logging
logger = logging.getLogger('morris_solr')
hdlr = logging.FileHandler('../logs/MorrisSolr.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


class SolrMorrisDecorator(AbstractMorrisDecorator):
    def __init__(self,solrURL):
        self.solrURL = solrURL
        self.solrCon = solr.SolrConnection(self.solrURL)
        self.deco_ids = 0
        self.assc_ids = 0
        self.cont_ids = 0
# These need to be turned into parameters, for greatest flexibility.
        self.DOCUMENT_TYPE = 'document_type'
        self.DECORATION_TYPE = 'decoration'
        self.CONTENT_TYPE = 'decorated_content'
        self.ASSOCIATION_TYPE = 'association'
        self.DECORATION_NAME = 'decoration_name'
        self.CONTENT_NAME = 'content_name'
        return

    def genDeco(self):
        self.deco_ids = self.deco_ids
        return str(datetime.datetime.utcnow())+"-"+str(self.deco_ids)

    def genAssc(self):
        self.assc_ids = self.assc_ids
        return str(datetime.datetime.utcnow())+"-"+str(self.assc_ids)

    def genCont(self):
        self.cont_ids = self.cont_ids
        return str(datetime.datetime.utcnow())+"-"+str(self.cont_ids)
    
    def deleteAll(self):
        try:
            self.solrCon.delete_query('document_type:'+self.ASSOCIATION_TYPE)
            self.solrCon.delete_query('document_type:'+self.CONTENT_TYPE)
            self.solrCon.delete_query('document_type:'+self.DECORATION_TYPE)
            self.solrCon.commit()
        except:
            print "deleteAll failure"
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print exc_type
            print exc_value
            print exc_traceback

    def deleteDecorations(self,decos):
        for d in decos:
            self.deleteDecoration(d)

    def deleteAssociation(self,decoration,content):
        try:
            logger.error('Call to deleteDecoration: '+decoration)
            d1 = 'document_type:'+self.ASSOCIATION_TYPE+' AND '+ \
                self.DECORATION_NAME+':'+urllib.quote(decoration) +' AND '+ \
                self.CONTENT_NAME+':'+urllib.quote(content)
            r1 = self.solrCon.delete_query(d1)
            self.solrCon.commit()
            logger.info('deleteDecoration Success! '+d1)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error('deleteDecoration Error: '+repr(exc_type))
            logger.error('deleteDecoration Error: '+repr(exc_value))
            logger.error('deleteDecoration Error: '+repr(exc_traceback))
            print exc_type
            print exc_value
            print exc_traceback

    def deleteDecoration(self,deco):
        try:
            logger.error('Call to deleteDecoration: '+deco)
            d1 = 'document_type:'+self.ASSOCIATION_TYPE+' AND '+ \
                self.DECORATION_NAME+':'+urllib.quote(deco)
            d2 = 'document_type:'+self.DECORATION_TYPE+' AND '+ \
                self.DECORATION_NAME+':'+urllib.quote(deco)
            logger.info('deleDecorationQueries = '+repr(d1)+'|'+repr(d2))
            r1 = self.solrCon.delete_query(d1)
            r2 = self.solrCon.delete_query(d2)
            self.solrCon.commit()
            logger.info('deleteDecoration responses! '+repr(r1)+'|'+repr(r2))
            logger.info('deleteDecoration Success! '+d1+'|'+d2)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error('deleteDecoration Error: '+repr(exc_type))
            logger.error('deleteDecoration Error: '+repr(exc_value))
            logger.error('deleteDecoration Error: '+repr(exc_traceback))
            print exc_type
            print exc_value
            print exc_traceback
        
    def createDecorations(self,decos):
        current = self.getAllDecorations()
        l = []
        for dec in decos:
            if (not dec in current):
                d = {}
                d[self.DOCUMENT_TYPE] = self.DECORATION_TYPE
                d[self.DECORATION_NAME] = urllib.quote(dec)
                logger.info('name before quote |'+dec+'|')
                logger.info('name after quote '+urllib.quote(dec))
                d['id'] = self.DECORATION_TYPE+self.genDeco();
                l.append(d)
        try:
            logger.info('adding decorations: '+repr(l))
            self.solrCon.add_many(l)
            self.solrCon.commit()
        except:
            print "create decoration failure"
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print exc_type
            print exc_value
            print exc_traceback

    def createContents(self,contents):
        current = self.getAllContents()
        l = []
        for con in contents:
            if (con not in current):
                d = {}
                d[self.DOCUMENT_TYPE] = self.CONTENT_TYPE
                d[self.CONTENT_NAME] = urllib.quote(con)
                d['id'] = self.CONTENT_TYPE+self.genCont()
                l.append(d)
        try:
            logger.info('adding content: '+repr(l))
            self.solrCon.add_many(l)
            self.solrCon.commit()
        except:
            print "create decoration failure"
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print exc_type
            print exc_value
            print exc_traceback

    def associateDecorationWithContentSingle(self,decoration,content):
        # WARNING! Remove this...this is for debugging
        self.createDecorations([decoration])
        self.createContents([content])
        l = []
        d = {}
        d[self.DOCUMENT_TYPE] = self.ASSOCIATION_TYPE
        d[self.DECORATION_NAME] = urllib.quote(decoration)
        d[self.CONTENT_NAME] = urllib.quote(content)
        d['id'] = self.ASSOCIATION_TYPE+self.genAssc()
        l.append(d)
        try:
            self.solrCon.add_many(l)
            self.solrCon.commit()
            logger.info('associated: '+repr(l))
        except:
            logger.error('Assocation failed: '+exc_type,exc_value,exc_taceback)
            print "assocation add failure"
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print exc_type
            print exc_value
            print exc_traceback

    def getContentsForDecoration(self,decoration):
        search = 'document_type:'+self.ASSOCIATION_TYPE
        search = search + ' AND ' + self.DECORATION_NAME+':'+urllib.quote(decoration)
        logger.info('getContenstForDecorationQuery = '+search)
        transactionDicts = self.solrCon.query(search,fl=self.CONTENT_TYPE,
                                              deftype='edismax')
        decos = []
        for hit in transactionDicts.results:
            if urllib.unquote(hit[self.DECORATION_NAME]) == decoration:
                decos.append(urllib.unquote(hit[self.CONTENT_NAME]).encode('ascii','ignore'))
        return sorted(decos)

    def getDecorationsForContent(self,content):
        search = 'document_type:'+self.ASSOCIATION_TYPE
        search = search + ' AND ' + self.CONTENT_NAME+':'+urllib.quote(content)
        transactionDicts = self.solrCon.query(search,fl=self.DECORATION_TYPE,
                                              deftype='edismax')
        decos = []
        for hit in transactionDicts.results:
            if urllib.unquote(hit[self.CONTENT_NAME]) == content:
                decos.append(urllib.unquote(hit[self.DECORATION_NAME]).encode('ascii','ignore'))
                
        return sorted(decos)

    def getAllDecorations(self):
        # Possibly this could be amended to look only 
        search = 'document_type:'+self.DECORATION_TYPE
        transactionDicts = self.solrCon.query(search,fl=self.DECORATION_NAME,
                                              deftype='edismax')
        decos = []
        for hit in transactionDicts.results:
            name = urllib.unquote(hit[self.DECORATION_NAME]).encode('ascii','ignore')
            if (name not in decos):
                decos.append(name)
        return sorted(decos)

    def getAllContents(self):
        search = 'document_type:'+self.CONTENT_TYPE
        transactionDicts = self.solrCon.query(search,fl=self.CONTENT_TYPE,
                                              deftype='edismax')
        decos = []
        for hit in transactionDicts.results:
            decos.append(urllib.unquote(hit[self.CONTENT_NAME]).encode('ascii','ignore'))
        return sorted(decos)
    def addClientDataDecoration(self,decoration,data_name,cd):
        full = self.getFullDecoration(decoration)
        l = []
        d = {}
        if (full is not None):
            d = full
            if 'score' in d: del d['score']
            d[data_name+"_t"] = cd
        else:
            d[self.DOCUMENT_TYPE] = self.DECORATION_TYPE
            d[self.DECORATION_NAME] = urllib.quote(decoration)
            d['id'] = self.DECORATION_TYPE+self.genDeco()
            d[data_name+"_t"] = cd
        l.append(d)
        try:
            self.solrCon.add_many(l)
            self.solrCon.commit()
        except:
            print "create decoration failure"
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print exc_type
            print exc_value
            print exc_traceback

    def getFullContent(self,content):
        search =  self.CONTENT_NAME+':'+urllib.quote(content)
        transactionDicts = self.solrCon.query(search,fl='*',
                                              deftype='edismax')
        decos = {}
        for hit in transactionDicts.results:
            # I should not have to do this, but there is a problem with 
            # escaping characters which is causing my tokens 
            # to match on partial matches!
            if (urllib.unquote(hit[self.CONTENT_NAME]) == content):
                return hit
        return None

    def getFullDecoration(self,content):
        search =  self.DECORATION_NAME+':'+urllib.quote(content)
        transactionDicts = self.solrCon.query(search,fl='*',
                                              deftype='edismax')
        decos = {}
        for hit in transactionDicts.results:
            # I should not have to do this, but there is a problem with 
            # escaping characters which is causing my tokens 
            # to match on partial matches!
            if (urllib.unquote(hit[self.DECORATION_NAME]) == content):
                return hit
        return None

    # def deleteContent(self,content):
    #     full = self.getFullContent(content)
    #     if (full is not None):
    #         self.solrCon.delete(full['id'])
    #         self.solrCon.commit()

    def addClientDataContent(self,content,data_name,cd):
        full = self.getFullContent(content)
        l = []
        d = {}
        if (full is not None):
            d = full
            if 'score' in d: del d['score']
            d[data_name+"_t"] = cd
        else:
            d[self.DOCUMENT_TYPE] = self.CONTENT_TYPE
            d[self.CONTENT_NAME] = urllib.quote(content)
            d['id'] = self.CONTENT_TYPE+self.genDeco()
            d[data_name+"_t"] = cd
        l.append(d)
        try:
            self.solrCon.add_many(l)
            self.solrCon.commit()
        except:
            print "create decoration failure"
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print exc_type
            print exc_value
            print exc_traceback

    def getClientDataDecorationName(self,decoration,data_name):
        search = 'document_type:'+self.DECORATION_TYPE
        search = search + ' AND ' + self.DECORATION_NAME+':'+urllib.quote(decoration)
        transactionDicts = self.solrCon.query(search,fl='*',
                                              deftype='edismax')
        for hit in transactionDicts.results:
            for key, value in hit.iteritems():
                if (key == data_name+'_t'):
                    return value
        return None

    def getClientDataContentName(self,content,data_name):
        search = 'document_type:'+self.CONTENT_TYPE
        search = search + ' AND ' + self.CONTENT_NAME+':'+urllib.quote(content)
        transactionDicts = self.solrCon.query(search,fl='*',
                                              deftype='edismax')
        for hit in transactionDicts.results:
            for key, value in hit.iteritems():
                if (key == data_name+'_t'):
                    return value
        return None

    def getClientDataContent(self,content):
        """
        Return the entire dictionary of client_data
        """
#        search = 'document_type:'+self.CONTENT_TYPE
#        search = search + ' AND ' + self.CONTENT_NAME+':'+urllib.quote(content)
        search =  self.CONTENT_NAME+':'+urllib.quote(content)
        transactionDicts = self.solrCon.query(search,fl='*',
                                              deftype='edismax')
        decos = {}
        for hit in transactionDicts.results:
            # I should not have to do this, but there is a problem with 
            # escaping characters which is causing my tokens 
            # to match on partial matches!
            if (urllib.unquote(hit[self.CONTENT_NAME]) == content):
                for key, value in hit.iteritems():
                    if (key.endswith('_t')):
                        decos[key[0:-2]] = value
        return decos

    def getClientDataDecoration(self,content):
        """
        Return the entire dictionary of client_data
        """
#        search = 'document_type:'+self.DECORATION_TYPE
#        search = search + ' AND ' + self.DECORATION_NAME+':'+urllib.quote(content)
        search = self.DECORATION_NAME+':'+urllib.quote(content)
        transactionDicts = self.solrCon.query(search,fl='*',
                                              deftype='edismax')
        decos = {}
        for hit in transactionDicts.results:
            # I should not have to do this, but there is a problem with 
            # escaping characters which is causing my tokens 
            # to match on partial matches!
            if (urllib.unquote(hit[self.DECORATION_NAME]) == content):
                for key, value in hit.iteritems():
                    if (key.endswith('_t')):
                        decos[key[0:-2]] = value
        return decos


    def exportContentsToDecorationsAsCSVWithClientDataColumns(self,columns):
        retval = ""
        retval = retval + ",".join(["Content","Decoration"]+['\"{0}\"'.format(c) for c in columns])+"\n"
        for c in self.getAllContents():
            dec = self.getDecorationsForContent(c)
            for d in dec: 
                retval = retval + '\"{0}\",\"{1}\"'.format(c,dec)
                clientdata = self.getClientDataContent(c)
                for col in columns:
                    if (col in clientdata):
                        retval = retval + ","
                        retval = retval + '\"{0}\"'.format(clientdata[col])
                retval = retval + "\n"
        return retval

    def exportDecorationsToContentsAsCSVWithClientDataColumns(self,columns):
        retval = ""
        retval = retval + ",".join(["Decoration","Content"]+['\"{0}\"'.format(c) for c in columns])+"\n"
        for d in self.getAllDecorations():
            con = self.getContentsForDecoration(d)
            for c in con: 
                retval = retval + '\"{0}\",\"{1}\"'.format(d,con)
                clientdata = self.getClientDataDecoration(d)
                for col in columns:
                    if (col in clientdata):
                        retval = retval + ","
                        retval = retval + '\"{0}\"'.format(clientdata[col])
                retval = retval + "\n"
        return retval

    def getRecordInteger(self,tag,recordkey):
        return
    def changeRecordInteger(self,tag,recordkey,delta):
        return
