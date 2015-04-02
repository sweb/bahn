# -*- coding: utf-8 -*-
"""
Created on Wed Apr 01 20:50:51 2015

@author: florian.mueller
"""
import urllib2

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
            
# Just a helper call to extract German train stations of category 1 and 2 from wikipedia. 
#url = "http://de.wikipedia.org/wiki/Liste_der_deutschen_Bahnh%C3%B6fe_der_Kategorie_1"
url = "http://de.wikipedia.org/wiki/Liste_der_deutschen_Bahnh%C3%B6fe_der_Kategorie_2"

request = urllib2.urlopen(url)
content = request.read()
request.close()

parser = WikiTableParser()
parser.feed(content)
parser.close()