#!/usr/bin/env python
# -*- coding: utf-8 -*-
# conver csv files into sql file

import csv
import sqlite3 as lite
import os
from os.path import isfile, join

import config


def main_function(CSV_DIR, SQL_DIR, sql_filename, append=True) :

	csv_files =  [ file for file in os.listdir(CSV_DIR) if isfile(join(CSV_DIR,file)) and '.csv' in file ]

	if not append and isfile(join(SQL_DIR,sql_filename)) :
		os.remove( SQL_DIR + sql_filename )
	conn = lite.connect( SQL_DIR + sql_filename )
	cursor = conn.cursor()

	f = open(config.sql_schema, 'r')
	schema = f.read()
	f.close()
	cursor.executescript(schema)

	for filename in csv_files :
		with open( CSV_DIR + filename, 'r') as f :
			reader = csv.reader(f)
			columns = next(reader)
			table_name = filename.split('.csv')[0]
			query = "INSERT INTO {0}  VALUES({1}) ;"
			query = query.format(table_name, ','.join('?' * len(columns)))
			for data in reader :
				cursor.execute(query,[ x.decode('utf-8') for x in data ])
			conn.commit()
	conn.close()




if __name__ == "__main__" :

	SQL_DIR = config.CAIRO_SQL
	CSV_DIR = config.CAIRO_CSV + "cairo_cleared_sample/"
	sql_filename = "cairo_cleared_sample.db"

	main_function(CSV_DIR, SQL_DIR, sql_filename, append=False)
	# if false and the file already exists it will erase it.
