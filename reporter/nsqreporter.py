import nsq
from .defaultreporter import defaultreporter


class nsqreporter(defaultreporter):
    def _init(self):
        self.hosts= self.conf.get(self.myname,"hosts").split(',')
        self.topic=self.conf.get(self.myname,"topic")
        print self.hosts, self.topic
        self.nsq= nsq.Writer(self.hosts)
        print self.nsq

    def _validateconf(self):
        if not self.conf.has_option(self.myname,"hosts"):
            raise ValueError("Section %r in config file does not have 'hosts' option" % self.myname)
        if not self.conf.has_option(self.myname,"topic"):
            raise ValueError("Section %r in config file does not have 'topic' option" % self.myname)

    def send_msg(self,doc_id,msg):
        self.nsq.pub(self.topic,msg)
        nsq.run()
