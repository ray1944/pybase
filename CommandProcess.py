import os
from subprocess import Popen
import subprocess as sbp
import sys
import re

class CommandProcess():

    processStatus = -1
    printBuffer = ''
    cmdStr = ''
    ignoreStrings = []
    numFile = 50000
    fnmPrefix = 'partnm-'
    ignorelines = ('^\s+$', '.*Dumping objects.*', '.*normal block.*', '.*Data:.*', '.*Object dump complete.*',
                   '.*Free Blocks.*', '.*Normal Blocks.*', '.*CRT Blocks.*', '.*Ignore Blocks.*',
                   '.*Client Blocks.*', '.*Largest number used:.*', '.*Total allocations:.*')
    svrslistpattern = '^\d+:\s+\w+\s+(\d+)\s+connected.*'
    servers = []
    ald = ''
    initparm = ''

    def __init__(self):
        self.processStatus = -1
        self.printBuffer = ''
        if sys.platform == 'win32':
            self.cmdpath = 'c:\\workspace\\aldon\\src\\client_lme\\aldcs\\'
            self.initparm = 'l13ssl:GrpPin/AppLarge/rls(000)::$1'
            self.targetpath = 'C:\\LMe000Daily\\GrpPin\\AppLarge\\rls(000)'
        elif sys.platform == 'linux2':
            self.cmdpath = '/opt/aldon/aldonlmc/current/bin/'
            self.targetpath = '/home/cheng/l08-dev'
            self.initparm = 'l13qua:GrpPin/AppLarge/rls\(000\)::\$1'
        else:
            print 'Unsupported OS ' + sys.platform + ' ' + os.name
            exit(-1)
        self.ald = self.cmdpath + 'ald'

    def run(self, cmd, consoleout = None):
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
                        for ignstr in self.ignorelines:
                            pattern = re.compile(ignstr)
                            if pattern.match(prtbuf) is not None:
                                prtbuf = ''
                                break
                        if len(prtbuf) > 0:
                            sys.stdout.write(prtbuf)
                            pattern = re.compile(self.svrslistpattern)
                            m = pattern.match(prtbuf)
                            if m is not None:
                                if m.group(1) is not None:
                                    self.servers.append(m.group(1))
                            if consoleout is not None:
                                consoleout.append(prtbuf)
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

    def init(self, repostr=''):
        if len(repostr) == 0:
            repostr = self.initparm
        cmd = self.ald + ' initialize ' + repostr
        ret = self.run(cmd)
        if ret != 0:
            print 'ald init failed'
            exit(ret)
        else:
            print 'initialized successfully'

    def signon(self, user='pcheng', password='nomoney@2018'):
        cmd = self.ald + ' signon -p ' + password + ' ' + user
        ret = self.run(cmd)
        if ret != 0:
            print 'signon failed'
            exit(ret)
        else:
            print 'signon successfully'

    def setdevpath(self):
        cmd = self.ald + ' setdevpath '
        ret = self.run(cmd)
        if ret != 0:
            print 'ald setdevpath failed'
            exit(ret)
        else:
            print 'setdevpath successfully'

    def getSvrID(self):
        cmd = self.ald + ' listsvrs'
        del self.servers[:]
        ret = self.run(cmd)
        if ret != 0:
            print 'get server id failed'
            return None
        else:
            return self.servers[:]

    def chtodir(self, path=''):
        curpath = os.getcwd()
        if len(path) == 0:
            path = self.targetpath

        # change to target path
        os.chdir(path)