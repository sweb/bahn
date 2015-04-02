# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import re


# This class implements an HTML parser in order to get the relevant delay data 
# from retrieved GET requests, issued to the web page of BAHN delays. It
# searches for <td> tags with the attribute class and values of 'train' and 
# 'ris'. It then identifies the train id and its delay.
# In addition it parses information from the file name itself like time and 
# train station.
class MyHTMLParser(HTMLParser):
  triggers = {"td": 0, "a": 0}
  rows = []
  currentTrainStation = ""
  currentYear = ""
  currentMonth = ""
  currentDay = ""
  currentTime = ""
  currentTrainType = ""
  currentTrainId = ""
  currentDelay = ""
  currentReason = ""
  currentAbort = "0"
  def handle_starttag(self, tag, attrs):
    if tag == "td":
      for attr in attrs:
        if attr[0] == "class" and attr[1] in ("train", "ris"):
          self.triggers["td"] = 1
          
    if tag == "a":
      self.triggers["a"] = 1
    
  def handle_endtag(self, tag):
    self.closeTrigger(tag, "td")    
    self.closeTrigger(tag, "a")

  def handle_data(self, data):
    if self.triggers['td'] == 1:
      if self.triggers['a'] == 1:
        matchTrain = re.search("(\\w{1,5})\\s*(\\d*)", data, flags=re.MULTILINE)
        if matchTrain != None:
          if self.currentTrainType != "":
            self.insertCurrentRow()
          self.currentTrainType = matchTrain.group(1)
          self.currentTrainId = matchTrain.group(2)
      matchDelay = re.search("\+(.*)", data)
      matchNoInfo = re.search("k.A.", data)
      matchReason = re.search("Grund: (.*)", data)
      matchAbort = re.search("Fahrt f.*llt aus", data)
      if matchDelay != None:
        self.currentDelay = matchDelay.group(1) 
      elif matchNoInfo != None:
        self.currentDelay = "ka"
      elif matchReason != None:
        self.currentReason = matchReason.group(1)
      elif matchAbort != None:
        self.currentAbort = "1"
      
            
  def insertCurrentRow(self):
    if self.currentDelay != "ka":
      self.rows.append((self.currentTrainStation, self.currentYear, 
                self.currentMonth, self.currentDay, self.currentTime,
                self.currentTrainType, self.currentTrainId, self.currentDelay, 
                self.currentReason, self.currentAbort))
    self.currentTrainType = ""
    self.currentTrainId = ""
    self.currentDelay = ""
    self.currentReason = ""
    self.currentAbort = "0"
    
  def getRows(self):
    return self.rows
    
  def parseFile(self, file):
    currentNumberOfTrainDelays = len(self.rows)
    htmlFile = open(file, "r")
    htmlText = HTMLParser.unescape.__func__(HTMLParser, htmlFile.read())
    htmlFile.close()
    self.parseFileName(file)
    self.feed(htmlText)
    self.insertCurrentRow()
    newNumberOfTrainDelays = len(self.rows)
    print "Number of added train delays:", str(newNumberOfTrainDelays - currentNumberOfTrainDelays)
    print "Current number of parsed train delays:", str(newNumberOfTrainDelays)
    
  def parseFileName(self, filename):
    match = re.search("query_(\\d{7})_(\\d{4})-(\\d{2})-(\\d{2})_(\\d{6}).html", filename)
    self.currentTrainStation = match.group(1)
    self.currentYear = match.group(2)
    self.currentMonth = match.group(3)
    self.currentDay = match.group(4)
    self.currentTime = match.group(5)
    
  def closeTrigger(self, tag, triggerName):
    if tag == triggerName:
      self.triggers[triggerName] = 0
