import os
from subprocess import Popen
import subprocess as sbp

class CommandProcess():

    processStatus = -1
    printBuffer = ''
    cmdStr = ''
    ignoreStrings = []

    def __init__(self, ignstrings):
        self.processStatus = -1
        self.printBuffer = ''

    def run(self):
        try:
            p = Popen(self.cmdStr, shell=True, stderr=sbp.STDOUT, stdout=sbp.PIPE)
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