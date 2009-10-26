
import comic, re

class Qwantz(comic.Comic):
    def __init__(self):
        comic.Comic.__init__(self)
        self.name = "Dinosaur Comics (Qwantz)"
        self.archive = 'http://www.qwantz.com/archive.php'
        self.arch_re = re.compile(r'<a href="(.*?comic=([0-9]*?))">(.*?)</a>:(.*?)</li>')
        self.root = 'http://questionablecontent.net/'
    def update_list(self):
        temp = self._download(self.archive)
        for match in re.findall(self.arch_re, temp):
            self.comics[int(match[1])] = (match[3].strip(), match[0], "")
        print self.comics
        """