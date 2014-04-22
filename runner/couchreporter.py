import couchdb as cou
from .defaultreporter import defaultreporter
#from reporter import reporter.defaultreporter.defaultreporter

class couchreporter(defaultreporter):
    def _init(self):
        url= self.conf.get(self.myname,"url")
        dbname=self.conf.get(self.myname,"db")
        print url, dbname
        self.srv= cou.Server(url)
        self.db= None
        if dbname in self.srv:
            print 'Open existing database'
            self.db= self.srv[dbname]
        else:
            print 'Create database'
            self.db= self.srv.create(dbname)

    def _validateconf(self):
        if not self.conf.has_option(self.myname,"url"):
            raise ValueError("Section %r in config file does not have 'url' option" % self.myname)

    def send_msg(self,doc_id,msg):
        self.db[doc_id]= msg

