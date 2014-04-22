#import sys, datetime, uuid, os, json, ConfigParser
#from importlib import import_module
#from socket import gethostname
import sys

rer=dict()

try:
    import reporter.defaultreporter
    reporter_registry={ 'default': reporter.defaultreporter.defaultreporter }
except Exception as e:
    print "Cannot import the default module reporter/defaultreporter.py"
    print "This is serious. Bailing out"
    

try:
    from couchreporter import couchreporter
    reporter_registry['couchrun']= couchreporter
except Exception as e:
    rer['couchrun']=e

try:
    from nsqreporter import nsqreporter
    reporter_registry['nsqrun']=nsqreporter
except Exception as e:
    rer['nsqrun']=e

try:
    from amqpreporter import amqpreporter
    reporter_registry['amqprun']=amqpreporter
except Exception as e:
    rer['amqprun']=e

def get_reporter(conf,name):
    if name in reporter_registry:
        return reporter_registry[name](conf,name)
    else:
        print "Error with reporter",name
        raise rer[name]
        



