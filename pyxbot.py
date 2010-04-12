#!/usr/bin/env python

import sys
from xml.sax.handler import ContentHandler
from xml.sax import make_parser

from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesNSImpl

class OSMHandler(ContentHandler):
    def __init__(self):
        # This is a bad state machine
        # This is a generic handler for nodes, ways or relations
        self.clear()
    def clear(self):
        self.tags = {}
        self.ways = []
        self.members = []
        self.attrs = {}
    def startElement(self, name, attrs):
        if name == 'tag':
            self.tags[attrs.get('k')] = attrs.get('v')
        elif name == 'way':
            self.ways.append(attrs.copy())
        elif name == 'member':
            self.members.append(attrs.copy())
        elif name == 'node' or name == 'way' or name == 'relation':
            self.attrs = attrs.copy()
    def endElement(self, name):
        self.clear()

parser = make_parser()
parser.setContentHandler(OSMHandler())
fname = sys.argv[1]
fh = open(fname)
parser.parse(fh)

