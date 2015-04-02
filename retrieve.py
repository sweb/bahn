# -*- coding: utf-8 -*-

import urllib2
import datetime
import time
import string
import grequests
import re

#url = "http://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=9646&rt=1&input=Münster(Westf)Hbf%238000263&boardType=dep&time=actual&productsFilter=11111&start=yes"
#M%C3%BCnster
#M%FCnster

# This function builds the request string by using an API call with a specific
# train station id.
def createRequestString(trainStation):
    url = string.join(("http://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=9646&rt=1&input=%23" 
    , urllib2.quote(trainStation) 
    , "&boardType=dep&time=actual&productsFilter=11111&start=yes"), sep="")
    return url
    
# This function stores the content of html requests on the local file system.
# It requires a timestamp and the train station id in order to store this
# information in the file name.
# No return values
def storeData( content, timestamp, trainStationId ):
    filename = "query_" + trainStationId + "_" + timestamp + ".html"
    file = open("data/" + filename, 'w')
    file.write(str(content))
    file.close()
    return

# Calculates the time difference between two points in time
def timeDifference( earlier, later ):
    return (later - earlier).total_seconds()


############################################################
#Program starts here
print "*** Hit CTRL+C to stop ***"
time.sleep(1)
#trainStations = ["Münster(Westf)Hbf", "Hamburg Hbf"]
trainStations  = ['008011102', '008011160', '008010255', '008011113', '008000080', '008010085', '008000085', '008000086', '008000098', '008000105', '008002553', '008002549', '008000152', '008000191', '008000105', '008003368', '008010205', '008000261', '008000262', '008000284', '008000096', '008000001', '008000002', '008000004', '008000010', '008000013', '008000023', '008000025', '008011306', '008010036', '008011118', '008010404', '008010405', '008010406', '008000036', '008000038', '008000041', '008000044', '008000049', '008000050', '008000055', '008010184', '008010073', '008000068', '008010089', '008096014', '008010101', '008000105', '008000107', '008000115', '008000114', '008000118', '008000124', '008000128', '008000142', '008010159', '008002548', '008000147', '008000149', '008000150', '008000156', '008000157', '008000162', '008000169', '008000189', '008000193', '008003200', '008000199', '008000206', '008000237', '008000236', '008000238', '008010224', '008000240', '008000244', '008000253', '008004158', '008000263', '008000271', '008000274', '008000275', '008000286', '008000290', '008000291', '008000294', '008000299', '008000302', '008012666', '008000309', '008000320', '008010304', '008000323', '008000073', '008000087', '008000134', '008000039', '008000168', '008000170', '008010366', '008000250', '008006552', '008000257', '008000266', '008000260']

# Removes the leading zeros from all Ids
for i in xrange(len(trainStations)):
    match = re.search("0*(\\d*)", trainStations[i])
    trainStations[i] = match.group(1)



while True:
    print("Request started...")
    trainStationRequests = (createRequestString(ts) for ts in trainStations)
    rs = (grequests.get(u) for u in trainStationRequests)
    executedRequests = grequests.map(rs)
    for i in xrange(len(executedRequests)):
        currentTime = datetime.datetime.now()
        timeOfQuery = datetime.datetime.strftime(currentTime, '%Y-%m-%d_%H%M%S')
        storeData(executedRequests[i].content, timeOfQuery, trainStations[i])
    time.sleep(300)
