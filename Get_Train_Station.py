# -*- coding: utf-8 -*-
"""
Created on Wed Apr 01 20:50:51 2015

@author: florian.mueller
"""

from HTMLParser import HTMLParser

class WikiTableParser(HTMLParser):
    tableTrigger = False
    aTagTrigger = False
    
    def handle_starttag(self, tag, attrs):
        #print(tag)
        if tag == "tr":
            self.tableTrigger = True
        if tag == "a":
            self.aTagTrigger = True
        
    def handle_endtag(self, tag):
        if tag == "tr":
            self.tableTrigger = False
        if tag == "a":
            self.aTagTrigger = False
        
    def handle_data(self, data):
        if self.tableTrigger and self.aTagTrigger:
            self.tableTrigger = False
            print(data)
            

    
url = "ts_cat2.html"
htmlFile = open(url, "r")
htmlText = htmlFile.read()
htmlFile.close()

parser = WikiTableParser()
parser.feed(htmlText)
parser.close()