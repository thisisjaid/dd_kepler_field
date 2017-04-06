#!/usr/bin/python3

import sys
import time
from astroquery.vizier import Vizier
import astropy.units as au

ddcollections = open("dd_target_collections.txt","r")

v = Vizier(columns=['AllWISE', 'RAJ2000', 'DEJ2000'])

for line in ddcollections:

	line = line.rstrip()
	ddtowise = open("data/dd_to_wise_ids_"+line+".txt","r")
	results = open("results/results_"+line+".txt","w")
	curline = 0
	nolines = len(ddtowise.readlines())
	ddtowise.seek(0)
	sys.stdout.write("Now processing collection %s \n" % line)

	for aline in ddtowise:
		curline += 1
		fields = aline.strip().split(",")
		qresult = v.query_object(fields[1],catalog=["AllWISE"],radius=0.001*au.deg) 
		array_result = qresult[0].as_array()
		print(fields[0],",",fields[1],",",array_result[0][1],",",array_result[0][2],sep='',file=results)
		progress = (curline / nolines)*100
		sys.stdout.write("\rNow %d%% done" % int(progress))
		time.sleep(1)
	ddtowise.close()
	results.close()
