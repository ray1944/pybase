'''running ald command to add 50000 parts into remote lme server'''
import partgen as pg


cmdpath = '/cygdrive/c/workspace/aldon/src/client_lme/aldcs/'
# cmd = cmdpath + 'ald'
cmd = 'ls -l'
ret = pg.runcmd(cmd)

if ret != 0:
    print 'command ended with error'
    exit(ret)
else:
    exit(0)
