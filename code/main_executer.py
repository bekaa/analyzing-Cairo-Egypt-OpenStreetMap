#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import get_map_sample
import exploring_map
import cleaning_map
import xml_to_csv
import csv_to_sql
'''
	this script lets you use the fuctions in the other scripts,
		you're free to execute each script on it's own, they are independent,
			but this script make things easier for you .

	steps will be   1. getting sample of the map,
					2. exploring the map,
					3. cleaning it,
					4. converting to csv,
					5. coverting the csv to sql.

*this script 'config' holds variables for the project directories , files  and some other variables
'''
#1. getting sample of the map. script : get_map_sample.py

#path to input OSM file.
input_map = config.cairo
#path to ouput OSM file
output_map_sample = config.cairo_sample
get_map_sample.main_function(config.cairo,config.cairo_sample,20)
# if the third parameter equal 10 then it will take every 10th element in the map.

#===============================================================================
#2. exploring the map. script : exploring_map.py
input_map_file = config.cairo_sample
output_folder = config.CAIRO_EXPLORING
# the function get_users returns a sorted list of tuples in the shape of {user:number_of_contributions}.
#	and if _saveToFile==True,it will write it into a file inside the output_folder
users = exploring_map.get_users(input_map_file,output_folder,_saveToFile=True)
# the function get_addr_tags return a list of lists of tuples., each list represents a key,
#		 and each tuple is  a value with it's number of occurence.
#			and if _saveToFile==True,it will write each list in to a file start with addr:... in the output folder.
_ = exploring_map.get_addr_tags(input_map_file,output_folder,_saveToFile=True)
#================================================================================================
#3. cleaning it. scirpt : cleaning_map.py
#path to input map file
input_map_file = config.cairo_sample
#path to where to save the cleaned map
cleaned_map = config.cairo_cleared_sample
cleaning_map.main_function(input_map_file ,cleaned_map,_saveToFile=True)
#============================================================================================
#4. converting the osm/xml map file into csv files.  script : xml_to_csv.py
# f
OSM_PATH = config.cairo_cleared_sample
DIR = config.CAIRO_CSV+"cairo_cleared_sample/"

# Note: Validation is ~ 10X slower. For the project consider using a small
# sample of the map when validating.
# the log file is for the validator, any errors will be wrote into it.
xml_to_csv.log_file = open(config.CAIRO_LOGS+"xml_to_csv.log",'a')
xml_to_csv.log_file.write("\n=====START======\n")
xml_to_csv.process_map(OSM_PATH, DIR, validate=False)
xml_to_csv.log_file.write("\n======END=======\n")
xml_to_csv.log_file.close()
#================================================================================================
#5. converting the csv into sql database file   script: csv_to_sql.py
SQL_DIR = config.CAIRO_SQL
CSV_DIR = config.CAIRO_CSV + "cairo_cleared_sample/"
sql_filename = "cairo_cleared_sample.db"

csv_to_sql.main_function(CSV_DIR, SQL_DIR, sql_filename, append=False)
	# if false and the file already exists it will erase it.
#=============================================================================================








