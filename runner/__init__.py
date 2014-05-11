
import sys, datetime, uuid, os, json, ConfigParser
from socket import gethostname
from subprocess import Popen, CalledProcessError


    
MSGTYPE='runner'


def tstamp():
    return datetime.datetime.utcnow().isoformat()


def get_reporter(conf):
    name= 'default' if not 'reporter' in conf else conf.reporter
    if name=="default":
        from .defaultreporter import defaultreporter as reporter
    elif name=="couchdb":    
        from .couchreporter import couchreporter as reporter
    else:
        print "Reporter name "+name+" unknown"
        exit(1)
    return reporter(conf)
            
def classify_stdout(outs):
    key=None
    val=None
    if len(outs)==0:
        return key,val
    try:
        val=json.loads( outs )
        key='stdjson'
        return key,val
    except Exception as e:
        pass
    key='stdout'
    val=outs
    return key,val



def cmd(args):
    files=["/etc/runner.cfg", os.path.expanduser("~/.runner.cfg") ]
    conf=ConfigParser.ConfigParser()
    conf.read(files)
    repclass= get_reporter(conf)
    rep=repclass(parser)
    doc_id= uuid.uuid4().hex
    m= { '_id':      doc_id,
         'type':     MSGTYPE,
         'hostname': gethostname(),
         'starttime':tstamp(),
         'cmd':      cmdargs,
         'state':    'started',
        }
    rep.send_msg(doc_id,m)
    print 'Started'

    # prepare stdout and stderr for the command and try run it
    stdoutf= "/tmp/"+doc_id+".stdout"
    stderrf= "/tmp/"+doc_id+".stderr"
    outf=os.open(stdoutf, os.O_WRONLY | os.O_CREAT)
    errf=os.open(stderrf, os.O_WRONLY | os.O_CREAT)
    retcode=-100
    try:
        p=Popen(cmdargs, 
                stdin=None,
                stdout=outf,
                stderr=errf)
        print 'Waiting'
        retcode=p.wait()
    except OSError as e:
        print e
        m['state']='oserror'
        m['statedesc']='OSError:'+e.strerror
    except Exception as e:
        print e
        m['state']='error'
        m['statedesc']=str(e)
    else:
        m['state']='done'
    print "Done"
    m['stoptime']= tstamp()
    os.close(outf)
    os.close(errf)
    m['retcode']= retcode

    output=open(stdoutf,"r").read()
    key,val = classify_stdout(output)
    if key:
       m[key]=val
    m['stderr']= open(stderrf,"r").read()
    rep.send_msg(doc_id,m)

    # Remove temporary stdout,stderr files
    os.unlink(stdoutf)
    os.unlink(stderrf)








