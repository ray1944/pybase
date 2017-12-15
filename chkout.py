'''running ald command to add 50000 parts into remote lme server'''
import partgen as pg
import os
import cmdsession

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
for num in range(cs.lastprtid, pg.numFile + 1):
    filenm = partprefix + str(num).zfill(5)
    cmd = pg.ald + ' checkout ' + filenm
    ret = pg.runcmd(cmd)
    if ret != 0:
        print 'ald checkout ' + filenm + ' failed.'
        cs.savesess()
        break
    else:
        print 'checkout ' + filenm + ' done'


exit(0)
