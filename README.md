# openstreetmap-udcity-s-Nanodegree-project
analyzing  cairo,Egypt 's osm file from openstreetmap.org.  
  
download the map osm file from the link [cairo](https://mapzen.com/data/metro-extracts/metro/cairo_egypt/)  

### a sample of the map could be found in /data/cairo/MAPS/cairo_sample.osm  in the project tree.

### read the report : cairo-egypt-osm-report.md ( also an html version is available cairo-egypt-osm-report.html )

the code folder contains the python scripts used in the report, they are used as follow :
  * config.py : contains variables to the path of used directories in the project, you need to change it before using any of the other scripts.
  * prettyprint.py : two functions writes data to a file, one for a dictionary and the other f a list/set .
  * get_map_sample.py : takes an osm map file and produce a sample of the map.
  * exploring_map.py : produces keys that starts with "addr" and their values of the map each key in a file.
  * cleaning_map.py : it cleans the add as explained in the report and produce new map.
  * xml_to_csv and schema.py : a code rewrite the xml file into a csv files, one file for each parent tag with some verfications using that schema.
  * csv_to_sql and schema.sql : create a database tables using the schema, then add the data from the csv files into these tables.
  * main_executer : this file explains how to use main functions of the other scripts and lets you use them without the need to run each script on it's one.
  
---------
#### in most of these scripts you will need to change the filename and the path to the input and output.
----------------
the 'data' folder contains subfolders and with empty files .  
actually it's a simulation of the project data directory tree that you should create or the config.py script will create it for you .
  
------------------------------

