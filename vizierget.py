#!/usr/bin/python3

import sys
from astroquery.vizier import Vizier
import astropy.units as au

ddwise = open("dd_wise.txt","r")
results = open("results.txt","w")
poop
v = Vizier(columns=['AllWISE', 'Jmag'])

curline = 0
nolines = len(ddwise.readlines())
ddwise.seek(0)

for line in ddwise:
	curline += 1
	fields = line.strip().split(",")
	qresult = v.query_object(fields[1],catalog=["AllWISE"],radius=0.001*au.deg) 
	array_result = qresult[0].as_array()
	print(fields[0],",",fields[1],",",array_result[0][1],sep='',file=results)
	progress = (curline / nolines)*100
	sys.stdout.write("\rNow %d%% done" % int(progress))
ddwise.close()
results.close()
