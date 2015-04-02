# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 21:34:30 2015

@author: florian.mueller
"""

import json
import urllib2
import re


def querySuggestionsByName(trainStationName):
    url = "http://reiseauskunft.bahn.de/bin/ajax-getstop.exe/dn?REQ0JourneyStopsS0A=1&REQ0JourneyStopsS0G=" + urllib2.quote(trainStationName)
    request = urllib2.urlopen(url)
    content = request.read()
    request.close()
    return content

def cleanSuggestions(rawSuggestions):
    match = re.search('SLs\\.sls=(\\{.*\\});SLs\\.showSuggestion\\(\\);', rawSuggestions)
    return match.group(1)
    
def selectTrainStationId(cleanSuggestions):
    decodedSuggestions = json.loads(unicode(cleanSuggestions, "ISO-8859-1"))['suggestions']
    if len(decodedSuggestions) < 1:
        return -1
    else:
        return json.loads(unicode(cleanSuggestions, "ISO-8859-1"))['suggestions'][0]['extId']
    
def getTrainStationId(trainStationName):
    rawSuggestions = querySuggestionsByName(trainStationName)
    cleanedSuggestions = cleanSuggestions(rawSuggestions)
    return selectTrainStationId(cleanedSuggestions)
    
    
trainStationNames = ['Berlin Gesundbrunnen', 'Berlin Hbf', 'Berlin Ostbahnhof', 'Berlin Südkreuz', 'Dortmund Hbf', 'Dresden Hbf', 'Düsseldorf Hbf', 'Duisburg Hbf', 'Essen Hbf', 'Frankfurt Hbf', 'Hamburg-Altona', 'Hamburg Hbf', 'Hannover Hbf', 'Karlsruhe Hbf', 'Köln Hbf', 'Köln Messe/Deutz', 'Leipzig Hbf', 'München Hbf', 'München Ost', 'Nürnberg Hbf', 'Stuttgart Hbf','Aachen Hbf', 'Aalen', 'Altenbeken', 'Aschaffenburg Hbf', 'Augsburg Hbf', 'Bad Oldesloe', 'Bamberg', 'Berlin Friedrichstraße', 'Berlin-Lichtenberg', 'Berlin Potsdamer Platz', 'Berlin-Spandau', 'Berlin-Wannsee', 'Berlin Zoologischer Garten', 'Bielefeld Hbf', 'Bietigheim-Bissingen', 'Bochum Hbf', 'Bonn Hbf', 'Braunschweig Hbf', 'Bremen Hbf', 'Bruchsal', 'Chemnitz Hbf', 'Cottbus', 'Darmstadt Hbf', 'Dresden-Neustadt', 'Düsseldorf Flughafen', 'Erfurt Hbf', 'Frankfurt Süd', 'Freiburg Hbf', 'Fulda', 'Fürth Hbf', 'Gelsenkirchen Hbf', 'Gießen', 'Göttingen', 'Hagen Hbf', 'Halle Hbf', 'Hamburg Dammtor', 'Hamburg-Harburg', 'Hamm ', 'Hanau Hbf', 'Heidelberg Hbf', 'Heilbronn Hbf', 'Herford', 'Hildesheim Hbf', 'Kaiserslautern Hbf', 'Kassel Hbf', 'Kassel-Wilhelmshöhe', 'Kiel Hbf', 'Koblenz Hbf', 'Lübeck Hbf', 'Ludwigshafen Hbf', 'Lüneburg', 'Magdeburg Hbf', 'Mainz Hbf', 'Mannheim Hbf', 'Mönchengladbach Hbf', 'München-Pasing', 'Münster Hbf', 'Neumünster', 'Neuss Hbf', 'Neustadt Hbf', 'Oberhausen Hbf', 'Offenburg', 'Oldenburg Hbf', 'Osnabrück Hbf', 'Pforzheim Hbf', 'Plochingen', 'Potsdam Hbf', 'Regensburg Hbf', 'Rosenheim', 'Rostock Hbf', 'Saarbrücken Hbf', 'Singen ', 'Solingen Hbf', 'Trier Hbf', 'Tübingen Hbf', 'Uelzen', 'Ulm Hbf', 'Weimar', 'Wiesbaden Hbf', 'Wolfsburg Hbf', 'Worms Hbf', 'Wuppertal Hbf', 'Würzburg Hbf']

trainStationIds = []
tsidsString = "["

for trainStationName in trainStationNames:
    id = getTrainStationId(trainStationName)
    trainStationIds.append(id)
    tsidsString = tsidsString + "'" + id + "', "  
    
print tsidsString