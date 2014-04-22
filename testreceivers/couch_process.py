#! /usr/bin/python

import sys, datetime, uuid
import couchdb as cou
from socket import gethostname
from subprocess import CalledProcessError, check_output

DB="joblog"



list_fun = '''function(doc) {
if (doc.type == 'runner')
  emit(doc)
}
'''    


def process():
    srv = cou.Server("http://srv3.koti:5984")
    db=None
    if DB in srv:
        print 'Open existing database'
        db=srv[DB]
    else:
        print 'Create database'
        db=srv.create(DB)


    for row in db.query(list_fun):
        print '-----'
        for k,v in row.key.iteritems():
            print "%20s : %s" % (k,v)
        db.delete(row.key)
    

if __name__ == '__main__':
    print 'Main'
    process()
    print 'Done'
