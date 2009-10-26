
import comic, re

class OOTS(comic.Comic):
    def __init__(self):
        comic.Comic.__init__(self)
        self.name = "Order of the Stick"
        self.archive = 'http://www.giantitp.com/comics/oots.html'
        self.arch_re = re.compile(r'<P class="ComicList">(.*?)<A href="(.*?)">(.*?)</A>')
        
    def update_list(self):
        temp = self._download(self.archive)
        for match in re.findall(self.arch_re, temp):
            self.comics[int(match[0])] = (match[2].strip(), match[1], None)
        print self.comics