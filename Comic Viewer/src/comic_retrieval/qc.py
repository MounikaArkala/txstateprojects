
import comic, re

class QustionableContent(comic.Comic):
    def __init__(self):
        comic.Comic.__init__(self)
        self.name = "Questionable Content"
        self.archive = 'http://questionablecontent.net/archive.php'
        self.arch_re = re.compile(r'<a href="(.*?)">Comic ([0-9]*?):(.*?)</a>')
        self.root = 'http://questionablecontent.net/'
    def update_list(self):
        temp = self._download(self.archive)
        for match in re.findall(self.arch_re, temp):
            self.comics[int(match[1])] = (match[2].strip(), match[0], None)
        print self.comics