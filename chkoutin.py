'''running ald command to add 50000 parts into remote lme server'''
import partgen as pg
import os
import cmdsession
import re

def isCheckoutTwiceTime(cmdout):
    ret = False
    regstr = ('Checking out:.*', 'AFF1108.*')
    conditions = []

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
pg.chtodir()
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
for num in range(cs.lastchkoutprtid + 1, pg.numFile + 1):
    filenm = partprefix + str(num).zfill(5)
    cmd = pg.ald + ' checkout ' + filenm
    consoleout = []
    ret = pg.runcmd(cmd, consoleout)
    if ret != 0:
        print 'ald checkout ' + filenm + ' failed.'
        #print consoleout[0]

        if (isCheckoutTwiceTime(consoleout)):
            cs.lastchkoutprtid = num
            cs.savesess()
            continue
        else:
            break
    else:
        print 'checkout ' + filenm + ' done'
        cs.lastprtid = num

if cs.lastchkoutprtid == pg.numFile:
    # check in
    for num in range(cs.lastchkinprtid, pg.numFile + 1):
        filenm = partprefix + str(num).zfill(5)
        cmd = pg.ald + ' checkin ' + filenm
        ret = pg.runcmd(cmd)
        if ret != 0:
            print 'ald checkin ' + filenm + ' failed. '
            cs.savesess()
            break
        else:
            print 'checkin ' + filenm + ' done'
            cs.lastchkinprtid = num

exit(0)
