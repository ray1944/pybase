'''import subprocess
import sys

cmdping  = 'ping baidu.com'
p = subprocess.Popen(cmdping, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
while True:
	out = p.stdout.read(1)
	p_status = p.poll()
	if out == '' and  p_status is not None:
		break
	if out != '':
		sys.stdout.write(out)
		sys.stdout.flush()


print 'command exit status/return code: ', p_status
'''
from partgen import runcmd

status = runcmd('ping baidu.com')
runcmd('ls -l')
