#!/usr/bin/env python
# -*- coding: utf-8 -*-
#convert xml map file  into csv type.
# read xml_to_csv_DOCUMENTATION.txt to know what's this script for ..

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus

#files
import config
import schema as schema



NODES_FILE            =  "nodes.csv"
NODE_TAGS_FILE        =  "nodes_tags.csv"
WAYS_FILE             =  "ways.csv"
WAY_NODES_FILE        =  "ways_nodes.csv"
WAY_TAGS_FILE         =  "ways_tags.csv"
RELATIONS_FILE        =  "relations.csv"
RELATION_MEMBERS_FILE =  "relation_members.csv"
RELATION_TAGS_FILE    =  "relation_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS             = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS        = ['id', 'key', 'value', 'type']
WAY_FIELDS              = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS         = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS        = ['id', 'node_id', 'position']
RELATION_FIELDS         = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
RELATION_MEMBERS_FIELDS = [ 'id', 'node_way_id', 'position', 'role', 'type' ]
RELATION_TAGS_FIELDS    = [ 'id', 'key', 'value', 'type' ]

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
				  relation_attr_fields=RELATION_FIELDS,
				  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
	"""Clean and shape node or way XML element to Python dict"""

	node_attribs     = {}
	way_attribs      = {}
	relation_attribs = {}
	tags             = []  # Handle secondary tags the same way for  node , way and relation elements
	way_nodes        = []
	relation_members = []

	nd_position = 0
	member_position = 0

	for child in element :
		#========
		# TAGS  ||
		#========
		if child.tag == 'tag' :
			tags.append(dict())
			key = child.attrib[ 'k' ] if 'k' in child.attrib else None
			if key and  PROBLEMCHARS.search(key) : key = None
			if key and  LOWER_COLON.search(key)  :
				key   = key.split(':')    if key  else None
				type_ = key[0]            if key  else None
				key   = ':'.join(key[1:]) if key  else None
			else :
				type_ = default_tag_type
			tags[len(tags)-1][ 'value' ] = child.attrib[ 'v' ]    if 'v'  in child.attrib   else None
			tags[len(tags)-1][ 'id' ]    = element.attrib[ 'id' ] if 'id' in element.attrib else None
			tags[len(tags)-1][ 'key' ]   = key
			tags[len(tags)-1][ 'type' ]  = type_

	 	#=============
		# way_nodes  ||
		#=============
		elif child.tag == 'nd' :
			way_nodes.append(dict())
			way_nodes[len(way_nodes)-1][ 'id' ]       = element.attrib[ 'id' ] if 'id'  in element.attrib else None
			way_nodes[len(way_nodes)-1][ 'node_id' ]  = child.attrib[ 'ref' ]  if 'ref' in child.attrib   else None
			way_nodes[len(way_nodes)-1][ 'position' ] = nd_position
			nd_position += 1

		#====================
		# relation_members  ||
		#====================
		elif child.tag == 'member' :
			relation_members.append(dict())
			index = len(relation_members)-1
			relation_members[index]['id']          = element.attrib['id'] if 'id'   in element.attrib else None
			relation_members[index]['node_way_id'] = child.attrib['ref' ] if 'ref'  in child.attrib   else None
			relation_members[index]['role']        = child.attrib['role'] if 'role' in child.attrib   else None
			relation_members[index]['type']        = child.attrib['type'] if 'type' in child.attrib   else None
			relation_members[index]['position']    = member_position
			member_position += 1

	#==================
	#=========
	# nodes  ||
	#=========
	if element.tag == 'node':
		for field in node_attr_fields :
			node_attribs[ field ] = element.attrib[ field ] if field in element.attrib else None

		return { 'node': node_attribs, 'node_tags': tags }

	#========
	# WAYS  ||
	#========
	elif element.tag == 'way':
		for field in way_attr_fields :
			way_attribs[ field ] = element.attrib[ field ] if field in element.attrib else None

		return { 'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags }
	#=============
	# RELATIONS  ||
	#=============
	elif element.tag == 'relation':
		for field in relation_attr_fields :
			relation_attribs[ field ] = element.attrib[ field ] if field in element.attrib else None

		return { 'relation': relation_attribs, 'relation_members': relation_members, 'relation_tags': tags }


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
	"""Yield element if it is the right type of tag"""

	context = ET.iterparse(osm_file, events=('start', 'end'))
	_, root = next(context)
	for event, elem in context:
		if event == 'end' and elem.tag in tags:
			yield elem
			root.clear()


def validate_element(element, validator, schema=SCHEMA):
	"""return False if element does not match schema"""
	if validator.validate(element, schema) is not True:
		field, errors = next(validator.errors.iteritems())
		message_string = "\nElement of type '{0}' has the following errors:\n{1}"
		error_string = pprint.pformat(errors)

		#raise Exception(message_string.format(field, error_string))
		log_file.write(message_string.format(field, error_string))
		print validator.errors
		return False
	return True


class UnicodeDictWriter(csv.DictWriter, object):
	"""Extend csv.DictWriter to handle Unicode input"""

	def writerow(self, row):
		super(UnicodeDictWriter, self).writerow({
			k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
		})

	def writerows(self, rows):
		for row in rows:
			self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, DIR, validate):
	#make sure that the "cairo_cleared_sample" directory exist, and if not make it.
	config.make_sure_directory_exists(DIR)

	"""Iteratively process each XML element and write to csv(s)"""

	with codecs.open(DIR+NODES_FILE           , 'w') as nodes_file,      \
		 codecs.open(DIR+NODE_TAGS_FILE       , 'w') as nodes_tags_file,  \
		 codecs.open(DIR+WAYS_FILE            , 'w') as ways_file,         \
		 codecs.open(DIR+WAY_NODES_FILE       , 'w') as way_nodes_file,     \
		 codecs.open(DIR+WAY_TAGS_FILE        , 'w') as way_tags_file,       \
		 codecs.open(DIR+RELATIONS_FILE       , 'w') as relations_file,       \
		 codecs.open(DIR+RELATION_MEMBERS_FILE, 'w') as relation_members_file, \
		 codecs.open(DIR+RELATION_TAGS_FILE   , 'w') as relation_tags_file      :


		nodes_writer            = UnicodeDictWriter(nodes_file           , NODE_FIELDS             )
		node_tags_writer        = UnicodeDictWriter(nodes_tags_file      , NODE_TAGS_FIELDS        )
		ways_writer             = UnicodeDictWriter(ways_file            , WAY_FIELDS              )
		way_nodes_writer        = UnicodeDictWriter(way_nodes_file       , WAY_NODES_FIELDS        )
		way_tags_writer         = UnicodeDictWriter(way_tags_file        , WAY_TAGS_FIELDS         )
		relations_writer        = UnicodeDictWriter(relations_file       , RELATION_FIELDS         )
		relation_tags_writer    = UnicodeDictWriter(relation_tags_file   , RELATION_TAGS_FIELDS    )
		relation_members_writer = UnicodeDictWriter(relation_members_file, RELATION_MEMBERS_FIELDS )

		nodes_writer.writeheader()
		node_tags_writer.writeheader()
		ways_writer.writeheader()
		way_nodes_writer.writeheader()
		way_tags_writer.writeheader()
		relations_writer.writeheader()
		relation_tags_writer.writeheader()
		relation_members_writer.writeheader()

		validator = cerberus.Validator()

		for element in get_element(file_in, tags=('node', 'way', 'relation')):
			el = shape_element(element)
			if el:
				if validate is True :
					if validate_element(el, validator) == False :
						continue

				if element.tag == 'node':
					nodes_writer.writerow(el['node'])
					node_tags_writer.writerows(el['node_tags'])
				elif element.tag == 'way':
					ways_writer.writerow(el['way'])
					way_nodes_writer.writerows(el['way_nodes'])
					way_tags_writer.writerows(el['way_tags'])

				elif element.tag == 'relation':
					relations_writer.writerow(el['relation'])
					relation_members_writer.writerows(el['relation_members'])
					relation_tags_writer.writerows(el['relation_tags'])


if __name__ == '__main__':

	OSM_PATH = config.cairo_cleared_sample
	DIR = config.CAIRO_CSV+"cairo_cleared_sample/"
	# Note: Validation is ~ 10X slower. For the project consider using a small
	# sample of the map when validating.
	log_file = open(config.CAIRO_LOGS+"xml_to_csv.log",'a')
	log_file.write("\n=====START======\n")
	process_map(OSM_PATH, DIR, validate=False)
	log_file.write("\n======END=======\n")
	log_file.close()

