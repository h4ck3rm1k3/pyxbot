#!/usr/bin/env python

import sys
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from pyxbot import OSMHandler
import re

BOTNAME = "pyxbot"
VERSION = "0.1"


from obj2xml import node2xml, way2xml, relation2xml

class KateBot(OSMHandler):

    def __init__(self, out):
        OSMHandler.__init__(self, out)
        self.seen = {}

        
    def selectElement(self):
        
        for k in ("addr:housenumber",
                  "addr:postcode" ,
                  "addr:street",
                  "building",
                  "addr:city"
              ):
            if not k  in self.tags:           
                return False
                
        if not ((self.name == "way" ) or (self.name == "node" )):
            return False
                
        vals = []
        for k in ("addr:housenumber",
                  "addr:postcode" ,
                  "addr:street",
                  "addr:city"):
            if k  in self.tags:
                vals.append(self.tags[k])
        n = "|".join(vals)

        ele = self.preDeleteElement()

        if (n not in self.seen):        
            self.seen[n] = [ele]
        else:
            self.seen[n].append(ele)


    def transformElement(self):
        """
        
        """
        #print str(self.__dict__)
        #self.deleteElement()

    def endDocument(self):
        for x in self.seen:
            ways = 0
            for y in self.seen[x]:
                if y.firstChild.tagName == "way":
                    ways = ways + 1
            if ways == 0 :
                continue

            for y in self.seen[x]:
                if y.firstChild.tagName == "node":                   
                    self.base.appendChild(y)

        OSMHandler.endDocument(self)

       

parser = make_parser()
fname = sys.argv[1]
out = open('kate-output.osc','w')
fh = open(fname)
parser.setContentHandler(KateBot(out))
parser.parse(fh)



##self.deleteElement()
