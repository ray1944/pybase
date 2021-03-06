import os
from subprocess import Popen
import subprocess as sbp
import sys
import re
import cmdsession

NUMFILE = 50000

def isCheckoutinTwiceTime(cmdout, ischeckout):
    ret = False
    regcheckoutstr = ('Checking out:.*', 'AFF1108.*')
    regcheckinstr = ('Checking in:.*', 'AFF1015.*')
    conditions = []
    regstr = regcheckoutstr
    if not ischeckout:
        regstr = regcheckinstr

    for idx in range(0, len(regstr)):
        conditions.append(False)

    for out in cmdout:
        for idx in range(0, len(regstr)):
            pattern = re.compile(regstr[idx])
            m = pattern.match(out)
            if m is not None:
                conditions[idx] = True

    for con in conditions:
        if not con:
            return False

    return True

class CommandProcess():

    processStatus = -1
    printBuffer = ''
    cmdStr = ''
    ignoreStrings = []
    fnmPrefix = 'partnm-'
    ignorelines = ('^\s+$', '.*Dumping objects.*', '.*normal block.*', '.*Data:.*', '.*Object dump complete.*',
                   '.*Free Blocks.*', '.*Normal Blocks.*', '.*CRT Blocks.*', '.*Ignore Blocks.*',
                   '.*Client Blocks.*', '.*Largest number used:.*', '.*Total allocations:.*')
    svrslistpattern = '^\d+:\s+\w+\s+(\d+)\s+connected.*'
    servers = []
    ald = ''
    initparm = ''

    def __init__(self, svrname = 'l13ssl', grp = 'GrpPin', app = 'AppLarge', release = 'rls', ver = '000', pd = '1'):
        self.setSvsParms(svrname, grp, app, release, ver, pd)

        self.processStatus = -1
        self.printBuffer = ''

        #initial parameter is like 'l13ssl:GrpPin/AppLarge/rls(000)::$1'
        if sys.platform == 'win32':
            self.cmdpath = 'c:\\workspace\\aldon\\src\\client_lme\\aldcs\\'
            self.targetpath = 'C:\\LMe000Daily\\GrpPin\\AppLarge\\rls(000)'
        elif sys.platform == 'linux2':
            self.cmdpath = '/opt/aldon/aldonlmc/current/bin/'
            self.targetpath = '/home/cheng/l08-dev'
            self.svrname = 'l13qua'
        else:
            print 'Unsupported OS ' + sys.platform + ' ' + os.name
            exit(-1)
        self.initparm = '{0}:{1}/{2}/{3}\({4}\)::\${5}'.format(self.svrname,
                                                               self.grp,
                                                               self.app,
                                                               self.release,
                                                               self.ver,
                                                               self.pd)
        self.ald = self.cmdpath + 'ald'
        self.sess = cmdsession.Cmdsession(self.targetpath)

    def setSvsParms(self, svrname = 'l13ssl', grp = 'GrpPin', app = 'AppLarge', release = 'rls', ver = '000', pd = '1'):
        self.svrname = svrname
        self.grp = grp
        self.app = app
        self.release = release
        self.ver = ver
        self.pd = pd

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
                                self.sess.log(prtbuf)
                            prtbuf = ''
                            sys.stdout.flush()

        except OSError:
            logmsg = 'the command {} is not exists'.format(cmd)
            print logmsg
            self.sess.log(logmsg)
            return -1
        except ValueError:
            logmsg= 'the command {} is not exists'.format(cmd)
            print logmsg
            self.sess.log(logmsg)
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
            logmsg = 'ald init failed'
            print logmsg
            self.sess.log(logmsg)
            exit(ret)
        else:
            logmsg = 'initialized successfully'
            print logmsg
            self.sess.log(logmsg)

    def signon(self, user='pcheng', password='nomoney@2018'):
        cmd = self.ald + ' signon -p ' + password + ' ' + user
        ret = self.run(cmd)
        if ret != 0:
            logmsg = 'signon failed'
            self.sess.log(logmsg)
            print logmsg
            exit(ret)
        else:
            logmsg = 'signon successfully'
            print logmsg
            self.sess.log(logmsg)

    def setdevpath(self):
        cmd = self.ald + ' setdevpath '
        ret = self.run(cmd)
        if ret != 0:
            logmsg = 'ald setdefpath failed'
            print logmsg
            self.sess.log(logmsg)
            exit(ret)
        else:
            logmsg = 'setdevpath successfully'
            print logmsg
        self.sess.log(logmsg)

    def getSvrID(self):
        cmd = self.ald + ' listsvrs'
        del self.servers[:]
        ret = self.run(cmd)
        if ret != 0:
            logmsg = 'get server id failed'
            print logmsg
            self.sess.log(logmsg)
            return None
        else:
            self.sess.log('get server id: {0}'.format(','.join(self.servers)))
            return self.servers[:]

    def chtodir(self, path=''):
        if len(path) == 0:
            path = self.targetpath

        # change to target path
        os.chdir(path)

    def addparts(self, start = 1, end = NUMFILE):
        if end is None:
            end = NUMFILE + 1

        for num in range(start, end + 1):
            filenm = self.fnmPrefix + str(num).zfill(5)
            cmd = self.ald + ' add -i ' + filenm
            ret = self.run(cmd)
            if ret != 0:
                logmsg = 'ald add {0} failed.'.format(filenm)
                print logmsg
                self.sess.log(logmsg)
                self.sess.savesess()
                break
            else:
                logmsg = 'adding {0} done'.format(filenm)
                print logmsg
                self.sess.log(logmsg)


    def getSession(self):
        return self.sess

    def chkout(self, start = 1, groupnum = 1):
        start = start != -1 and start or self.sess.lastchkoutprtid
        for num in range(start, NUMFILE + 1, groupnum):
            filelist = []
            filelistsize = (num + groupnum) < NUMFILE and num + groupnum or NUMFILE
            for idx in range(num, filelistsize):
                filelist.append(self.fnmPrefix + str(idx).zfill(5))
            cmd = '{0} checkout {1}'.format(self.ald, ' '.join(filelist))
            consoleout = []
            ret = self.run(cmd, consoleout)
            if ret != 0:
                print cmd + ' failed.'
                if isCheckoutinTwiceTime(consoleout, True):
                    self.sess.lastchkoutprtid = num
                    self.sess.savesess()
                    continue
                else:
                    self.sess.lasterrors = consoleout
                    self.savesess()
                    msg = 'Checkout error: ' + '\n'.join(consoleout)
                    self.sess.log(msg)
                    raise Exception(msg)
            else:
                msg = 'checkout ' + ','.join(filelist) + ' done'
                print msg
                self.sess.log(msg)
                self.sess.lastchkoutprtid = num + groupnum
                self.sess.savesess()

    def chkin(self, start = 1, groupnum = 1):
        start = start != -1 and start or self.sess.lastchkinprtid
        for num in range(start, NUMFILE + 1, groupnum):
            filelist = []
            filelistsize = (num + groupnum) < NUMFILE and num + groupnum or NUMFILE
            for idx in range(num, filelistsize):
                filelist.append(self.fnmPrefix + str(idx).zfill(5))
            cmd = '{0} checkin {1}'.format(self.ald, ' '.join(filelist))
            consoleout = []
            ret = self.run(cmd, consoleout)
            if ret != 0:
                msg = 'ald checking in {0} failed.'.format(' '.join(filelist))
                if (isCheckoutinTwiceTime(consoleout, False)):
                    self.sess.lastchkinprtid = num
                    self.sess.savesess()
                    continue
                else:
                    self.sess.lasterrors = consoleout
                    self.sess.savesess()
                    print msg
                    self.sess.log(msg)
                    raise Exception(msg)

            else:
                msg = 'checking in {0} done.'.format(' '.join(filelist))
                self.sess.lastchkinprtid = num + groupnum
                self.sess.savesess()
                print msg
                self.sess.log(msg)

    def resetSession(self):
        self.sess.lastchkinprtid = 0
        self.sess.lastchkoutprtid = 0
        self.sess.savesess()