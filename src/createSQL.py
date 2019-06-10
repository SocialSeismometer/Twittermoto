# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:14:36 2019

@author: Arsalan
"""

# IMPORTING MODULES
import sqlite3

# SET DATA DIRECTORY
DIR = './Data'
#FILE = '/allCountries.txt'
FILE = '/cities500.txt'
file = '{}{}'.format(DIR, FILE)

# CONNECTING TO DATABASE
conn = sqlite3.connect('cities500.db')
c = conn.cursor()

# FUNCTIONS
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS tableTest(geonameid INTEGER ,	name TEXT , asciiname TEXT, alternatenames TEXT,latitude REAL , longitude REAL, feature_class TEXT, feature_code TEXT, country_code TEXT, cc2 TEXT, admin1_code TEXT, admin2_code TEXT, admin3_code TEXT, admin4_code TEXT, population INTEGER, elevation REAL, dem INTEGER, timezone TEXT, modification_date TEXT)')
    
def data_entry(lineList):
    geonameid ,	name , asciiname , alternatenames ,latitude , longitude , feature_class , feature_code , country_code , cc2 , admin1_code , admin2_code , admin3_code , admin4_code , population , elevation , dem , timezone , modification_date \
     = lineList
    try:
        population = int(population)
    except:
        population  = 'NaN'
    try:
        elevation = float(elevation)
    except:
        elevation = 'NaN'
    try:
        dem = int(dem)
    except:
        dem = 'NaN'
    c.execute(" INSERT INTO tableTest (geonameid ,	name , asciiname , alternatenames ,latitude , longitude , feature_class , feature_code , country_code , cc2 , admin1_code , admin2_code , admin3_code , admin4_code , population , elevation , dem , timezone , modification_date) \
              VALUES( ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ?) "  , \
              (int(geonameid) ,	name , asciiname , alternatenames , float(latitude) , float(longitude) , feature_class , feature_code , country_code , cc2 , admin1_code , admin2_code , admin3_code , admin4_code , population , elevation , dem , timezone , modification_date) )
    
# MAIN     
create_table()
with open(file, encoding="utf8") as f:
    for line in f:
        lineList = line.split('\t')
        data_entry(lineList)
conn.commit()        
c.close()
conn.close()

        