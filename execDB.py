# resetDB.py
import sqlite3
import sys
import codecs
import csv
from csv import reader

## YOU CAN USE THIS FILE TO RUN ANY SQLITE CODE

DATABASE = 'KyotoMap.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.text_factory = str
    return db

if(len(sys.argv) < 2):
	print("To use this program to run sqlite code type: python execDB -e <SQLITE CODE FILENAME>")
	print("To use this program to insert data in a table from .csv file type: python execDB -i <TABLE NAME> <CSV FILE NAME>")
else:
	if(sys.argv[1] == "-e" and len(sys.argv) > 2):
		filename = sys.argv[2]
		file = open(filename, "r")
		dbCode = file.read()

		print("Running sqlite code...")
		cursor = get_db().executescript(dbCode)
		get_db().commit()
		cursor.close()
		print("Done!")

	elif(sys.argv[1] == "-i" and len(sys.argv) > 3):
		
		print("Inserting into table "+sys.argv[2]+"...")
		
		table = sys.argv[2].lower()
		
		csvfilename = sys.argv[3]
		
		csvfile = codecs.open(csvfilename, 'r', 'UTF-8')
		csv_reader = reader(csvfile)
		next(csv_reader) #skipping header row
		
		data = list(map(tuple, csv_reader))

		if(table == "location"):
			cursor = get_db()
			cursor.executemany("INSERT INTO 'location' ('pname', 'jpname', 'lat', 'lon', 'category', 'label', 'description', 'popularity') VALUES (?,?,?,?,?,?,?,?)", data)
			cursor.commit()
			cursor.close()

		elif(table == "poly"):
			cursor = get_db()
			cursor.executemany("INSERT INTO 'poly' ('pid', 'lat', 'lon') VALUES (?,?,?)", data)
			cursor.commit()
			cursor.close()
		
		elif(table == "locationimages"):
			cursor = get_db()
			cursor.executemany("INSERT INTO 'locationImages' ('pid', 'imageUrl') VALUES (?,?)", data)
			cursor.commit()
			cursor.close()

		else:
			print("Table "+sys.argv[2]+" does not exist in the database.")
			print("Tables that exist are:")
			print("location, poly, locationimages")

		print("Program done. Byebye!!")
	else:
		print("To use this program to run sqlite code type: python execDB -e <SQLITE CODE FILENAME>")
		print("To use this program to insert data in a table from .csv file type: python execDB -i <TABLE NAME> <CSV FILE NAME>")