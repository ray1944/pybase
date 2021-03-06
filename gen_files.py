# -*- coding: UTF-8 -*-
import partgen as pg
import FileNotFoundError

def genFiles():
	for id in range(40056, pg.numFile + 1):
		filenm = pg.fnmPrefix + str(id).zfill(5)
		try:
			with open(filenm, 'w') as f_obj:
				f_obj.write(filenm + '\n')
		except FileNotFoundError:
			print("file generated failed " + filenm)


genFiles()
