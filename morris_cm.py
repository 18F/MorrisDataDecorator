
class ExampleMorrisContentManager:
    """This is a simple example Morris Content Manager.  It is exists so 
That we can have something to test in advance of you writing your own
version of this abstract class that actually does something useful.
"""
    def __init__(self):
        self.keys = ["nothing uploaded"+str(x) for x in range(20)]
        self.urls = ["nothing uploaded"+str(x) for x in range(20)]

    def getNthModularly(self,n):
        return self.keys[n % len(self.keys)]

    def next(self,key):
        idx = self.keys.index(key)
        return self.getNthModularly(idx+1)
        
    def prev(self,key):
        idx = self.keys.index(key)
        return self.getNthModularly(idx-1)

    def getAUsefulKey(self):
        return self.keys[0]

    def getHTML(self,key):
        idx = self.keys.index(key)
        return self.urls[idx]

    def loadUrlsFromText(self,text):
        """Load urls or other targets from separate lines in the text
        """
        self.urls = text.split('\n') 
        if "" in self.urls: self.urls.remove("")
        self.keys = [str(x) for x in range(len(self.urls))]

