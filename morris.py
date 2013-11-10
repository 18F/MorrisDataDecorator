# Morris is a decorator system for decorating objects that may not be under full control of the 
# implementor of the Morris system.  Decorations including scoring, tagging, and creating portfolios.

from abc import ABCMeta,abstractproperty
import sys

class AbstractMorrisDecorator:
    """Morris is a decorator system for decorating content objects that may not be under full control of the 
implementer of the Morris system.  Decorations including scoring, tagging, and creating portfolios.
"""
    __metaclass__ = ABCMeta
    @abstractproperty
    def createDecorations(self,decos):
        """ Idempotently create empty decoration records if they do not already exist.
        """

    @abstractproperty
    def createContents(self,contents):
        """ Idempotently create empty content records if they do not already exist.
        """

    @abstractproperty
    def associateDecorationWithContentSingle(self,decoration,content):
        """ Assoction the decoration to the content """

    @abstractproperty
    def getContentsForDecoration(self,decoration):
        """ Return a collection of content having this decoration
        """

    @abstractproperty
    def getDecorationsForContent(self,content):
        """ Return a collection of content having this decoration
        """

    @abstractproperty
    def getAllDecorations(self):
        """ Return all of the decorations
        """

    @abstractproperty
    def getAllContents(self):
        """ Return all of the contents
        """

    @abstractproperty
    def addClientDataDecoration(self,decoration,data_name,cd):
        """ create a decoration, with an arbitary client data field
        """

    @abstractproperty
    def getClientDataDecorationName(self,decoration,data_name):
        """ Return clident data stored under data_name for this decoration
        """

    @abstractproperty
    def addClientDataContent(self,content,data_name,cd):
        """ Create clident data stored under data_name for this content
        """

    @abstractproperty
    def getClientDataContentName(self,content,data_name):
        """ Return clident data stored under data_name for this content
        """
    @abstractproperty
    def getClientDataContent(self,content):
        return "not implemented"
    @abstractproperty
    def getClientDataDecoration(self,content):
        return "not implemented"

    def exportDecorationsAsCSV(self):
        """
    Export the decorations only without the contents
        """
        retval = ""
        retval = retval + "Decoration\n"
        for p in self.getAllDecorations():
            retval = retval + '\"{0}\"\n'.format(p)
        return retval

    def exportContentsAsCSV(self):
        """
    Export the contents only without associations
        """
        retval = ""
        retval = retval + "Content\n"
        for p in self.getAllContents():
            retval = retval + '\"{0}\"\n'.format(p)
        return retval


    def exportContentsToDecorationsAsCSV(self):
        retval = ""
        retval = retval + "Content,Decoration\n"
        for c in self.getAllContents():
            d = self.getDecorationsForContent(c)
            retval = retval + '\"{0}\",\"{1}\"\n'.format(c,d)
        return retval

    def exportDecorationsToContentsAsCSV(self):
        retval = ""
        retval = retval + "Decoration,Content\n"
        for d in self.getAllDecorations():
            c = self.getContentsForDecoration(d)
            retval = retval + '\"{0}\",\"{1}\"\n'.format(d,c)
        return retval

    # @abstractproperty
    # def exportContentsToDecorationsAsCSV(self):
    #     """
    # Export the entire datastore as a CSV file 
    #     """

    # @abstractproperty
    # def exportDecorationsToContentsAsCSV(self):
    #     """
    # Export the entire datastore as a CSV file 
    #     """

    @abstractproperty
    def exportContentsToDecorationsAsCSVWithClientDataColumns(self,columns):
        """
    Export the entire datastore as a CSV file, adding columns from ClientData where it exists.
        """

    @abstractproperty
    def exportDecorationsToContentsAsCSVWithClientDataColumns(self,columns):
        """
    Export the entire datastore as a CSV file, adding columns from ClientData where it exists.
        """

# I will have to clean this up later!
    @abstractproperty
    def getRecordInteger(self,tag,recordkey):
        """ get an associated integer
        """

    @abstractproperty
    def changeRecordInteger(self,tag,recordkey,delta):
        """ increment or decrement an associate integer
        """



class InMemoryMorrisDecorator(AbstractMorrisDecorator):
    def __init__(self):
        """
The basic structure is a doubly-indexed table that assocations content to decorations and vice versa.
You can perform O(1) lookup of either the decoration strings to find the decorated content, or the 
content keys to find the decorations.

Note that you can create unassociated content; that is, you can create a decoration which 
is not attached to any content, and you can declare content that has no decorations (though
presumably there will be undeclared content as well.)

Note that the ClientData is meant to be "uninterpreted" by the Morris system.  That is, it has 
no meaning, it is merely a convenient place to store Data on behalf of the Client.  However, it 
is echoed back in both the CSV export and through the API, so it is in particularly valuable 
to the system which also uses the ContentManagement system.

The "Integer" system is somewhat different.  It is not intended to be "client data", in that 
it is typed, initialized to zero, and is modified by direct delta incrementation or decrementation.
This is in fact the only justification for making it distinct from the ClientData.
        """
# decorationToContent maps strings ("decorations") to list keys managed by the morris_cm module (optionally)
        self.initializeAll()

    def initializeAll(self):
        self.decorationToContent = {}    # A dictionary of strings to content keys
        self.decorationToClientData = {} # A dictionary of dictionaries of strings
        self.decorationToIntegers = {}   # A dictionary of dictionaries of integers

        self.contentToDecoration = {}    # A dictionary of strings to decoration keys
        self.contentToClientData = {}    # A dictionary of dictionaries of strings
        self.contentToIntegers = {}      # A dictionary of dictionaries of integers

# Not sure what to do about this, really needs to be generalized as a Decoration.
        self.integerTagMaps = {}

    def deleteAll(self):
        self.initializeAll()
        
    def createDecorations(self,decos):
        for d in decos:
            if (d not in self.decorationToContent):
                self.decorationToContent[d] = [];
        return decos

    def createContents(self,contents):
        for c in contents:
            if (c not in self.contentToDecoration):
                self.contentToDecoration[c] = [];
                
    def associateDecorationWithContentSingle(self,decoration,content):
        self.createDecorations([decoration])
        self.createContents([content])
        if (decoration not in self.contentToDecoration[content]):
            self.contentToDecoration[content].append(decoration)
        if (content not in self.decorationToContent[decoration]):
            self.decorationToContent[decoration].append(content)

    def getContentsForDecoration(self,decoration):
        return sorted(self.decorationToContent.get(decoration,[]))

    def getDecorationsForContent(self,content):
        return sorted(self.contentToDecoration.get(content,[]))

    def getAllDecorations(self):
        return self.decorationToContent.keys()

    def getAllContents(self):
        return self.contentToDecoration.keys()

    def addClientDataDecoration(self,decoration,data_name,cd):
        if (decoration not in self.decorationToClientData):
            self.decorationToClientData[decoration] = {}
        self.decorationToClientData[decoration][data_name] = cd

    def getClientDataDecorationName(self,decoration,data_name):
        return self.decorationToClientData[decoration][data_name]

    def getClientDataContent(self,content):
        return "not implemented"
    def getClientDataDecoration(self,content):
        return "not implemented"

    def addClientDataContent(self,content,data_name,cd):
        if (content not in self.contentToClientData):
            self.contentToClientData[content] = {}
        self.contentToClientData[content][data_name] = cd

    def getClientDataContentName(self,content,data_name):
        return self.contentToClientData[content][data_name]

    def exportContentsToDecorationsAsCSVWithClientDataColumns(self,columns):
        retval = ""
        retval = retval + ",".join(["Content","Decoration"]+['\"{0}\"'.format(c) for c in columns])+"\n"
        print "All Contents = "+repr(self.getAllContents())
        for c in self.getAllContents():
            d = self.getDecorationsForContent(c)
            retval = retval + '\"{0}\",\"{1}\"'.format(c,d)
            for col in columns:
                if (c in self.contentToClientData):
                    retval = retval + ","
                    retval = retval + '\"{0}\"'.format(self.contentToClientData[c][col])
            retval = retval + "\n"
        return retval

    def exportDecorationsToContentsAsCSVWithClientDataColumns(self,columns):
        retval = ""
        retval = retval + ",".join(["Decoration","Content"]+['\"{0}\"'.format(c) for c in columns])+"\n"
        for d in self.getAllDecorations():
            c = self.getContentsForDecoration(d)
            retval = retval + '\"{0}\",\"{1}\"'.format(d,c)
            for col in columns:
                retval = retval + ","
                if (d in self.decorationToClientData):
                    retval = retval + '\"{0}\"'.format(self.decorationToClientData[d][col])
            retval = retval + "\n"
        return retval

# I will have to clean this up later!
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


