# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 14:36:45 2019

@author: Arsalan
"""

# IMPORTING MODULES
from ssGeoCoder import GeoCoder
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ["PROJ_LIB"] ="C:\\Users\\Arsalan\\Anaconda3\\pkgs\\proj4-5.2.0-ha925a31_1\\Library\\share"; #fixr
from mpl_toolkits.basemap import Basemap
from itertools import chain

# INPUT
dbfilename    = 'cities500'  # filename of database to be created/queried
sourcefilename =  dbfilename     # filename of the text file containing data source
# ---------------------------MAIN---------------------------------------------

# instantiating GeoCoder class
myGeoCoder = GeoCoder(dbfilename,sourcefilename)

# creating database
myGeoCoder.create_database()

# Open Connection
myGeoCoder.open_connection()

# searching for lat long
result = myGeoCoder.get_Lat_Long(['rawalpindi'])

# close connection
myGeoCoder.close_connection()

# Plotting coordinates on a map
'''
To enable plotting on map the Basemap package needs to be installed by typing 
the following lines in anaconda command prompt: $ conda install basemap
Ref: https://jakevdp.github.io/PythonDataScienceHandbook/04.13-geographic-data-with-basemap.html
'''
def draw_map(m, scale=0.2):
    # draw a shaded-relief image
    m.shadedrelief(scale=scale)
    
    # lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(-90, 90, 13))
    lons = m.drawmeridians(np.linspace(-180, 180, 13))

    # keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)
    
    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')

fig = plt.figure(figsize=(8, 6), edgecolor='w')
m = Basemap(projection='cyl', resolution=None,
            llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180, )
draw_map(m)
if result:
    # Map (long, lat) to (x, y) for plotting
    x, y = m(result[2],result[1])
    plt.plot(x, y, 'ok', markersize=5)
    plt.text(x, y, result[0], fontsize=12);

