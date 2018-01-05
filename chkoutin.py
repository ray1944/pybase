
'''running ald command to add 50000 parts into remote lme server'''
import os
import cmdsession
from CommandProcess import CommandProcess as CP

curpath = os.getcwd()
pg = CP(ver='001')
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


# ald add parts and check in
for idx in range(1, 100):
    pg.sess.log('{0} time(s) check in/out begins'.format(idx))
    pg.chkout(-1, 10)
    pg.chkin(-1, 10)
    pg.resetSession()
    pg.sess.log('{0} time(s) check in/out ends'.format(idx))



exit(0)
