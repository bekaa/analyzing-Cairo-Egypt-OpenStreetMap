#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
this script holds variables for the project directories , files  and some other variables
'''


# directories used [all directories variables' names are capital]
# change the PROJ_DIR to yours , also make sure that all the sub-directories are exist
# the project doesn't make any directories, it assumes that they are already made.
# so You need to make the three folders  .../project/data/cairo
#	and inside the folder 'cairo' 5 more folders [ exploration - MAPS - CSV - LOG - SQL ]
#  and download the cairo osm map file as " ../project/cairo/MAPS/cairo_egypt.osm"

# hint : the function make_sire_directory_exists will make all sub directories inside project if you didn't do it

import os
import errno
#make sure that the  directory exist, and if not make it.
def make_sure_directory_exists(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise


PROJ_DIR = "/home/SOME_USER/..../project/"
DATA_DIR = PROJ_DIR + "data/"
CAIRO_DATA_DIR = DATA_DIR + "cairo/"
CAIRO_EXPLORING = CAIRO_DATA_DIR + "exploration/"
CAIRO_MAPS = CAIRO_DATA_DIR + "MAPS/"
CAIRO_CSV = CAIRO_DATA_DIR + "CSV/"
CAIRO_LOGS = CAIRO_DATA_DIR + "LOG/"
CAIRO_SQL = CAIRO_DATA_DIR + "SQL/"

# files
cairo = CAIRO_MAPS + "cairo_egypt.osm"
cairo_cleared = CAIRO_MAPS + "edited_cairo_map.osm"
cairo_cleared_sample = CAIRO_MAPS+"edited_cairo_map_sample.osm"
sql_schema = PROJ_DIR + "code/schema.sql"

make_sure_directory_exists(DATA_DIR)
make_sure_directory_exists(CAIRO_DATA_DIR)
make_sure_directory_exists(CAIRO_EXPLORING)
make_sure_directory_exists(CAIRO_MAPS)
make_sure_directory_exists(CAIRO_CSV)
make_sure_directory_exists(CAIRO_LOGS)
make_sure_directory_exists(CAIRO_SQL)



#***************************************************************************************************************
# streets for cairo, banha, giza used in the file addr_cleaning
cairo_streets = [u"مصر الجديدة",u"New Cairo",u"العباسية",u"قاهرة",u"مدينة نصر",u"Cairo",u"الزاوية الحمراء",u"Al Manteqah Al Oula",u"Zamalek",u"البساتين",u"القاهرة",u"Kairo",u"Maadi",u"Orabi",u"التجمع الأول",u"Mokkatam",u"ma`adi",u'cairo']
banha_streets = [u"دار السلام",u"قليوب",u"العبور",u"Manial",u"الشروق",u"الماظة",u"Banha"]
giza_streets = [u"مدينة 6 أكتوبر",u"October 6",u"جيزه",u"الجيزة",
	u"giza",u"Giza",u"العبور",u"Haram",u"هرم",u"october 6",u"Gizeh",u"GIza",
	u"6th October City",u"6th of October",u"6th of October City",u"حى النسايم",u'6 October',u'6 october']
#*********************************************************************************************************
