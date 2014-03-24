#!/usr/bin/env python

import sys
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from pyxbot import OSMHandler
import re

BOTNAME = "dupnodesbot"
VERSION = "0.1"

from obj2xml import node2xml, way2xml, relation2xml

class KateBot(OSMHandler):
    """
    Delete duplicate nodes
    """
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
                
        if not self.name == "node" :
            return False

        for k in ("addr:housename",
                  "amenity",
                  "landuse",
                  "shop",
                  "facebook",
                  "name", # skip over named items
        ):
            if k in self.tags:
                return False
                
        vals = []
        
        for k in ("addr:housenumber",
                  "addr:postcode" ,
                  "addr:street",
                  "addr:suite",
                  "addr:city"):
            if k  in self.tags:
                vals.append(self.tags[k])
        n = "|".join(vals)



        if (n not in self.seen):        
            self.seen[n] = 1
        else:
            self.deleteElement()            
      

parser = make_parser()
fname = sys.argv[1]
out = open('kate-output.osc','w')
fh = open(fname)
parser.setContentHandler(KateBot(out))
parser.parse(fh)



##self.deleteElement()
