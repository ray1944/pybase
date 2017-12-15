from subprocess import Popen
import subprocess as sbp
import sys
import re
import os

numFile = 50000
fnmPrefix = 'partnm-'
ignorelines = ('^\s+$', '.*Dumping objects.*', '.*normal block.*', '.*Data:.*', '.*Object dump complete.*',
               '.*Free Blocks.*', '.*Normal Blocks.*', '.*CRT Blocks.*', '.*Ignore Blocks.*',
               '.*Client Blocks.*', '.*Largest number used:.*', '.*Total allocations:.*')
svrslistpattern = '^\d+:\s+\w+\s+(\d+)\s+connected.*'
cmdpath = 'c:\\workspace\\aldon\\src\\client_lme\\aldcs\\'
ald = cmdpath + 'ald'
initparm = 'l13ssl:GrpPin/AppLarge/rls(000)::$1'
targetpath = 'C:\\LMe000Daily\\GrpPin\\AppLarge\\rls(000)'
servers = []


def runcmd(cmd):
    p_status = -1
    prtbuf = ''
    try:
        p = Popen(cmd, shell=True, stderr=sbp.STDOUT, stdout=sbp.PIPE)
        while True:
            out = p.stdout.read(1)
            p_status = p.poll()
            if out == '' and p_status is not None:
                break
            else:
                prtbuf += out

                if out == '\n':
                    # sys.stdout.write(prtbuf)
                    for ignstr in ignorelines:
                        pattern = re.compile(ignstr)
                        if pattern.match(prtbuf) is not None:
                            prtbuf = ''
                            break
                    if len(prtbuf) > 0:
                        sys.stdout.write(prtbuf)
                        pattern = re.compile(svrslistpattern)
                        m = pattern.match(prtbuf)
                        if m is not None:
                            if m.group(1) is not None:
                                servers.append(m.group(1))
                        prtbuf = ''
                        sys.stdout.flush()

    except OSError:
        print 'the command {} is not exists'.format(cmd)
        return -1
    except ValueError:
        print 'Invalid parameters'
        return -2
    # except CalledProcessError:
    #     print 'Command {} exit with errors'.format(cmd)

    return p_status

def init(repostr = ''):
    if len(repostr) == 0:
        repostr = initparm
    cmd = ald + ' initialize ' + repostr
    ret = runcmd(cmd)
    if ret != 0:
        print 'ald init failed'
        exit(ret)
    else:
        print 'initialized successfully'

def signon(user = 'pcheng', password = 'nomoney@2018'):
    cmd = ald + ' signon -p ' + password + ' ' + user
    ret = runcmd(cmd)
    if ret != 0:
        print 'signon failed'
        exit(ret)
    else:
        print 'signon successfully'

def setdevpath():
    cmd = ald + ' setdevpath '
    ret = runcmd(cmd)
    if ret != 0:
        print 'ald setdevpath failed'
        exit(ret)
    else:
        print 'setdevpath successfully'

def getSvrID():
    cmd = ald + ' listsvrs'
    del servers[:]
    ret = runcmd(cmd)
    if ret != 0:
        print 'get server id failed'
        return None
    else:
        return servers[:]

def chtodir(path = ''):
    curpath = os.getcwd()
    if len(path) == 0:
        path = targetpath

    # change to target path
    os.chdir(path)
