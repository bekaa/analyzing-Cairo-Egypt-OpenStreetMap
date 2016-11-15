#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
this one gets a sample from a map
'''
import xml.etree.cElementTree as ET
import pprint
import re
import operator
import prettyprint
import config



def get_element(osm_file, tags=('node', 'way', 'relation')):
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def main_function(OSM_FILE,SAMPLE_FILE,k=10) :
	with open(SAMPLE_FILE, 'wb') as output:
	    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	    output.write('<osm>\n  ')

	    # Write every kth top level element
	    for i, element in enumerate(get_element(OSM_FILE)):
	        if i % k == 0:
	            output.write(ET.tostring(element, encoding='utf-8'))

	    output.write('</osm>')



if __name__ == "__main__" :
	OSM_FILE = config.cairo
	SAMPLE_FILE = config.cairo_sample
	k = 10 # Parameter: take every k-th top level element

	#change it to true to run
	if False :
		main_function(OSM_FILE,SAMPLE_FILE,k)

