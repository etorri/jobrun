
class defaultreporter:
    def __init__(self,conf,name):
        self.myname=name
        self.conf=conf
        self.validateconf()
        self._init()

    def _init(self):
        pass
    def _validateconf(self):
        pass
    def validateconf(self):
        if not self.conf.has_section(self.myname):
            raise ValueError("No section %r in config file" % self.myname )
        self._validateconf()
    def send_msg(self,doc_id,msg):
        print '--------------'
        print 'doc_id',doc_id
        print msg

