
class defaultreporter:
    def __init__(self,conf):
        self.conf=conf
        self._init()

    def _init(self):
        pass

    def send_msg(self,doc_id,msg):
        print '--------------'
        print 'doc_id',doc_id
        print msg

