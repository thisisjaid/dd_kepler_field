#!/usr/bin/python3

import sys
import time
import os.path
from astroquery.vizier import Vizier
import astropy.units as au

ddcollections = open("dd_target_collections.txt","r")

v = Vizier(columns=['AllWISE', 'RAJ2000', 'DEJ2000', '2Mkey'])
v2 = Vizier(columns=['KIC', 'fv', '2Mkey'])
v3 = Vizier(columns=['EPIC'])


for line in ddcollections:

	line = line.rstrip()

	if os.path.isfile("data/dd_to_wise_ids_"+line+".txt"): 
		ddtowise = open("data/dd_to_wise_ids_"+line+".txt","r")
		results = open("results/results_"+line+".txt","w")
		print("DD_ID,WISE_ID,RAJ2000,DEJ2000,KIC_ID,KIC_FOV,2MKEY_MISMATCH,K2_EPIC",file=results)
		curline = 0
		nolines = len(ddtowise.readlines())
		ddtowise.seek(0)
		sys.stdout.write("Now processing collection %s \n" % line)

		for aline in ddtowise:
			curline += 1
			fields = aline.strip().split(",")

			qresult = v.query_object(fields[1],catalog=["AllWISE"],radius=0.001*au.deg) 
			if qresult:
				array_result = qresult[0].as_array()
				resultline = str(fields[0])+","+str(fields[1])+","+str(array_result[0][1])+","+str(array_result[0][2])
			else:
				resultline = str(fields[0])+","+str(fields[1])+",NF,NF,NF,NF,NF,NF"
				print(resultline,file=results)
				progress = (curline / nolines)*100
				continue
			
			time.sleep(1)

			qresult2 = v2.query_object(fields[1],catalog=["V/133"],radius=0.001*au.deg) 
			if qresult2:
				array_result2 = qresult2[0].as_array()
				if str(array_result[0][3]) == str(array_result2[0][2]):
					resultline = resultline+","+str(array_result2[0][1])+","+str(array_result2[0][0])+",0"
				else:
					resultline = resultline+","+str(array_result2[0][1])+","+str(array_result2[0][0])+",1"	
			else:
				resultline = resultline+",NA,NA,NA"
			
			time.sleep(1)
			
			qresult3 = v3.query_object(fields[1],catalog=["EPIC"],radius=0.001*au.deg)
			if qresult3:
				array_result3 = qresult3[0].as_array()
				resultline = resultline+","+str(array_result3[0][0])
			else:
				resultline = resultline+",NA"

			print(resultline,file=results)
			progress = (curline / nolines)*100
			sys.stdout.write("\rNow %d%% done" % int(progress))
			time.sleep(1)
		ddtowise.close()
		results.close()
