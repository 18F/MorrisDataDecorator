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
    def deleteDecorations(self,decos):
        """ Delete arguments and all associations.
        """

    @abstractproperty
    def createContents(self,contents):
        """ Idempotently create empty content records if they do not already exist.
        """

    @abstractproperty
    def associateDecorationWithContentSingle(self,decoration,content):
        """ Assoction the decoration to the content """

    @abstractproperty
    def deleteAssociation(self,decoration,content):
        """ deleteAssociation """

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



