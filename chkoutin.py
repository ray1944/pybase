
'''running ald command to add 50000 parts into remote lme server'''
import partgen as pg
import os
import cmdsession
import re
from CommandProcess import CommandProcess as CP

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



curpath = os.getcwd()
# pg.chtodir()
pg = CP()
curpath1 = os.getcwd()
# ald initialize
pg.init()

# ald signon
pg.signon()

# ald setdevpath
#pg.setdevpath()

cs = cmdsession.Cmdsession(curpath)
cs.serverids = pg.getSvrID()
cs.savesess()
#cs.lastprtid = 1

# ald add parts and check in
partprefix = 'partnm-'
consoleout = []
for num in range(cs.lastchkoutprtid + 1, pg.numFile + 1):
    filenm = partprefix + str(num).zfill(5)
    cmd = pg.ald + ' checkout ' + filenm

    ret = pg.run(cmd, consoleout)
    if ret != 0:
        print 'ald checkout ' + filenm + ' failed.'
        #print consoleout[0]

        if (isCheckoutinTwiceTime(consoleout, True)):
            cs.lastchkoutprtid = num
            cs.savesess()
            continue
        else:
            cs.lasterrors = consoleout
            cs.savesess()
            exit -1
    else:
        print 'checkout ' + filenm + ' done'
        cs.lastchkoutprtid = num
        cs.savesess()

if cs.lastchkoutprtid == pg.numFile:
    # check in
    for num in range(cs.lastchkinprtid, pg.numFile + 1):
        filenm = partprefix + str(num).zfill(5)
        cmd = pg.ald + ' checkin ' + filenm
        consoleout = []
        ret = pg.run(cmd, consoleout)
        if ret != 0:
            print 'ald checkin ' + filenm + ' failed. '

            if (isCheckoutinTwiceTime(consoleout, False)):
                cs.lastchkinprtid = num
                cs.savesess()
                continue
            else:
                cs.lasterrors = consoleout
                cs.savesess()
                exit(-1)

        else:
            print 'checkin ' + filenm + ' done'
            cs.lastchkinprtid = num
            cs.savesess()

exit(0)
