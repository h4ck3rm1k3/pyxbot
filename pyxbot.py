#!/usr/bin/env python

import sys
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from obj2xml imort node2xml, way2xml, relation2xml

BOTNAME = "pyxbot"
VERSION = "0.2"

class OSMHandler(ContentHandler):
    """This is a base OSMHandler class which sets up the XML parsing, etc.

    You will want to override the selectElement and transformElement
    functions"""
    def __init__(self, out):
        self.out = out
        "Initiate the SAX state machine"
        self.clear()

    # These methods are quick n dirty. Very dirty.
    def _emit_node(self):
        "Output a node"
        return node2xml(self).to_xml()

    def _emit_way(self):
        "Output a way"
        return way2xml(self).to_xml()

    def _emit_relation(self):
        "Output a relation"
        return relation2xml(self).to_xml()

    def emit(self):
        "Output the current element"
        if self.name == 'node':
            self._emit_node()
        elif self.name == 'way':
            self._emit_way()
        elif self.name == 'relation':
            self._emit_relation()

    def clear(self):
        "Initialize the state machine"
        self.name = None
        self.tags = {}
        self.nodes = []
        self.members = []
        self.attrs = {}

    def startElement(self, name, attrs):
        "This function is called at the start of the element (as per SAX)"
        if name == 'node':
            self.name = 'node'
            self.attrs = attrs.copy()
        elif name == 'way':
            self.name = 'way'
            self.attrs = attrs.copy()
        elif name == 'relation':
            self.name = 'relation'
            self.attrs = attrs.copy()
        elif name == 'tag':
            self.tags[attrs.get('k')] = attrs.get('v')
        elif name == 'member':
            self.members.append(attrs.copy())
        elif name == 'nd':
            self.nodes.append(attrs.get('ref'))

    def selectElement(self):
        """Select whether or not we care about the OSM object (True or
        False). Override this function in your handler"""
        return False

    def transformElement(self):
        """Transform the element. Override this function in your
        handler"""
        pass
    def modifyElement(self):
        """Modify this element"""
        self.out.write('<modify version="%s" generator="%s">\n' %
                       (VERSION, BOTNAME))
        self.emit()
        self.out.write("</modify>\n")
    def deleteElement(self):
        """Returns the string to delete the element.  Please use with
        caution!"""
        self.out.write('<delete version="%s" generator="%s">\n' %
                       (VERSION, BOTNAME))
        self.emit()
        self.out.write('</delete>\n')
    def endElement(self, name):
        """As per the SAX handler, this method is where any work is
        done. You may want to override it, but probably not"""
        if name == 'node' or name == 'way' or name == 'relation':
            if self.selectElement():
                self.transformElement()
                self.modifyElement()
            self.clear()

class PassThroughHandler(OSMHandler):
    def selectElement(self):
        return True

class MyHandler(OSMHandler):
    def selectElement(self):
        return self.attrs.get('id') == "55319624"

parser = make_parser()
parser.setContentHandler(MyHandler(sys.stdout))
fname = sys.argv[1]
out = sys.stdout
fh = open(fname)
parser.parse(fh)
