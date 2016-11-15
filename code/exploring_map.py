#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script extracts data from the map ,
the function get_addr_tags() for each different key "k" have "addr:" in the tag "tag",
 a file will be created which will have two columns (csv)
  the first one is the value (V) and the second is the occurence of that value in the map
	* all the output files will start with "tags_.."


the function get_users prints out to some file All the users contributed in the map and
 how many times their names are found.

'''
import xml.etree.cElementTree as ET
import re
import operator


import prettyprint
import config


#this function checks if the input text is in English characters or in some other language
def isEnglish(text):
	try :	text.decode("ascii")
	except UnicodeDecodeError:	return False
	else : return True

def get_users(filename,output_folder,_saveToFile=False):
	users = dict()
	for _, element in ET.iterparse(filename):
		if 'user' in element.attrib :
			user = element.attrib['user'].encode('utf-8').strip()
			if user in users :
				users[user] += 1
			else :
				users[user] = 1
	users = sorted(users.items(), key = operator.itemgetter(1),reverse=True)
	if _saveToFile : prettyprint._dict(output_folder+"users",users,'name','edits')
	return users



def get_addr_tags(filename,output_folder,_saveToFile=False) :
	keys = dict()
	for _,element in ET.iterparse(filename, events=("start","end")):
		for child in element.iter("tag") :
			k = child.attrib['k']
			v = child.attrib['v'].encode("utf-8")
			#if 'addr:' in k  :
			if k in ['addr:city','addr:housenumber','addr:postcode','addr:country']:
				if k in keys :
					if v in keys[k]:
						keys[k][v] +=1
					else :
						keys[k][v] = 1
				else :
					keys[k] = dict()
					keys[k][v] = 1
	for dic in keys :
		keys[dic] = sorted(keys[dic].items(), key=operator.itemgetter(1),reverse=True)
	if _saveToFile :
		for dic in keys :
			#prettyprint._list(config.CAIRO_EXPLORING+"tags_"+dic, keys[dic].keys())
			prettyprint._dict(output_folder+"tags_"+dic, keys[dic], 'key', '#occurance')
	return keys


if __name__ == "__main__":
	input_map_file = config.cairo
	output_folder = config.CAIRO_EXPLORING

	# change to True to run ..
	if False :
		users = get_users(input_map_file,output_folder,_saveToFile=False)
		_ = get_addr_tags(input_map_file,output_folder,_saveToFile=False)



