from subprocess import Popen
import subprocess as sbp
import sys
numFile = 50000
fnmPrefix = 'partnm-'


def runcmd(cmd):
    p_status = -1
    try:
        p = Popen(cmd, shell=True, stderr=sbp.STDOUT, stdout=sbp.PIPE)
        while True:
            out = p.stdout.read(1)
            p_status = p.poll()
            if out == '' and p_status is not None:
                break
            else:
                sys.stdout.write(out)
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

