'''running ald command to add 50000 parts into remote lme server'''
from CommandProcess import CommandProcess as CP
import os
import cmdsession

# cs = cmdsession.Cmdsession(curpath)
pg = CP()
cs = pg.getSession()
pg.chtodir()

# ald initialize
#pg.init()

# ald signon
pg.signon()

# ald setdevpath
# pg.setdevpath()


cs.serverids = pg.getSvrID()
cs.savesess()

# ald add parts and check in
pg.addparts(49999)


exit(0)
