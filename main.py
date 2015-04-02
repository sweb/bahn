# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 15:55:35 2015

@author: florian.mueller
"""

import BahnDelayParser
import os
import csv

# Location of html files
PATH_TO_DATA = "C:/dev/repositories/python/bahn/data"
# Parser for the html files
parser = BahnDelayParser.MyHTMLParser()
# Lists all files in relevant folder
listOfFiles = os.listdir(PATH_TO_DATA)
print "Number of identified files:", len(listOfFiles)

# Run through all files and parse their content. The results are stored in the
# parser.
for f in listOfFiles:
    print "Parsing file", f
    parser.parseFile(PATH_TO_DATA + "/" + f)
    parser.close()

# After parsing all files, get the parsed data rows
rows = parser.getRows()

# Store the data in a csv file as basis for data analysis.
with open("parsedDelays.csv", "wb") as csvfile:
    writer = csv.writer(csvfile, delimiter = ';')
    writer.writerow(['Trainstation','Year', 'Month', 'Day', 'Time', 
    'TrainType', 'TrainId', 'Delay', 'Reason', 'Abort'])
    for r in rows:
        writer.writerow(r)