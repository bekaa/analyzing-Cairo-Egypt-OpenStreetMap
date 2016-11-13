#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
this script  checks for all faulty data I mentioned in the project_report.md
	 and then decide wether to reject, correct or keep the data as it is
	 and then write the data into a new file  .

	 the name and path of the output file can be changed in the variable config.cairo_cleared in config.py script.
'''
import xml.etree.cElementTree as ET
import re
import operator

import prettyprint
import config

postcode_matching = re.compile("^\d{1,5}$")
housenumber_matching = re.compile("(^[a-zA-Z]?\d{1,5}$)|(^\d{1,5}[a-zA-Z]?$)")


# the three four functions clears the city,Country,housenmber and postcode .
def clean_city(city):
	for street in  config.banha_streets :
		if street in city :
			return "Banha",False
	for street in config.giza_streets :
		if street in city :
			return "Giza",False
	for street in config.cairo_streets :
		if street in  city :
			return "Cairo",False
	return city,True

def clean_country(country):
	if country in ['EG','ET'] :
		return 'EG',False
	return country,True

def clean_housenumber(num):
	if '-' in num :
		nums = num.split('-')
		if '[' in nums[0] :
			nums[0] = nums[0][1:]
		if ']' in nums[len(nums)-1] :
			nums[len(nums)-1] = nums[len(nums)-1][:-1]
	else :
		nums = [num]
	for item in nums :
		if not housenumber_matching.match(item) :
			return num,True
	return num,False

def clean_postcode(code):
	if postcode_matching.match(code) :
		return code,False
	return code,True

# this function takes the map file, iterate over each element, clean it then yield it to the main function 'clean_and_save'
def clean_and_parse(filename,tags=('node','way','relation') ) :
	context = iter(ET.iterparse(filename, events=('start','end')))
	_,root = next(context)
	for event, element in context :
		skip = False
		for child in element.iter("tag"):
			k = child.attrib['k'].encode('utf-8').strip()
			if k == 'addr:city' :
				v = unicode(child.attrib['v']).strip()
				child.attrib['v'],skip = clean_city(v)
			elif k == 'addr:country':
				v = child.attrib['v'].encode('utf-8').strip()
				child.attrib['v'],skip = clean_country(v)
			elif k == 'addr:housenumber':
				v = child.attrib['v'].strip()
				child.attrib['v'],skip = clean_housenumber(v)
			elif k == 'addr:postcode':
				v = child.attrib['v'].strip()
				child.attrib['v'],skip = clean_postcode(v)
			if skip : break
		if skip :
			root.clear()
			continue
		elif event == 'end' and element.tag in tags:
			yield element
			root.clear()

#main function
def clean_and_save(input_file,output_file=None,_saveToFile=True) :
	if _saveToFile :
		with open(output_file, 'wb') as output:
			output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
			output.write('<osm>\n  ')
			for element in clean_and_parse(input_file) :
				output.write(ET.tostring(element, encoding='utf-8'))
			output.write('</osm>')
	else : #else if I wan to do some calc or print it out
		for element in clean_and_parse(input_file) :
			print ET.tostring(element,encoding='utf-8')



if __name__ == "__main__" :
		# usage : clean_and_save(input_map_file, [output_map_file, _saveToFile=bool])
		#change to True to run
		if False:
			clean_and_save(config.cairo ,config.cairo_cleared,_saveToFile=True)



