
import urllib

class Comic(object):
    def __init__(self):
        #subclasses should call super's __init__ just in case this
        #function changes in the future to actually do something.
        self.comics = {}
        self.name = ""
        pass
        
    def update_list(self):
        #get a list of every comic, in the form
        #{number: (title, link, date)}
        # and set self.comics
        pass
        
    def retrieve(self, number):
        # download the comic for a specific number and return it.
        # they can take care of caching / displaying / etc. themselves.
        pass
        
    def _download(self, address, binary=False):
        if binary:
            u = urllib.urlopen(address, "b").read()
        else:
            u = urllib.urlopen(address).read()
        return u