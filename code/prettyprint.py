#!/usr/bin/env python
'''
this file has to functions _dict, and _list
and what it does is to write _dict or a _list into the input file.
'''
import csv

def _dict(filename,data,key="key",value="value") :
	with open(filename,'w') as f :
		writer = csv.writer(f)
		writer.writerow([key,value])
		writer.writerows(data)

def _list(filename,data) :
	with open(filename,'w') as f :
		for item in data :
			f.write(item+"\n")
