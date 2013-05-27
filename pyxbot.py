#!/usr/bin/env python

import sys
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from obj2xml import node2xml, way2xml, relation2xml
from xml.dom.minidom import Element, Document

BOTNAME = "pyxbot"
VERSION = "0.6"

class OSMHandler(ContentHandler):
    """This is a base OSMHandler class which sets up the XML parsing, etc.

    You will want to override the selectElement and transformElement
    functions"""
    def __init__(self, out):
        self.out = out
        "Initiate the SAX state machine"
        self.clear()
        # This will hold our output document
        self.doc = Document()
        self.base = self.doc.createElement('osmChange')
        self.base.setAttribute('version', VERSION)
        self.base.setAttribute('generator', BOTNAME)
        self.doc.appendChild(self.base)

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
            self.attrs = dict(attrs.copy())
        elif name == 'way':
            self.name = 'way'
            self.attrs = dict(attrs.copy())
        elif name == 'relation':
            self.name = 'relation'
            self.attrs = dict(attrs.copy())
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
        ele = self.doc.createElement('modify')
        if self.name == 'node':
            ele.appendChild(node2xml(self))
        elif self.name == 'way':
            ele.appendChild(way2xml(self))
        elif self.name == 'relation':
            ele.appendChild(relation2xml(self))
        self.base.appendChild(ele)

    def deleteElement(self):
        """Returns the string to delete the element.  Please use with
        caution!"""
        ele = self.doc.createElement('delete')
        if self.name == 'node':
            ele.appendChild(node2xml(self))
        elif self.name == 'way':
            ele.appendChild(way2xml(self))
        elif self.name == 'relation':
            ele.appendChild(relation2xml(self))
        self.base.appendChild(ele)

    def endElement(self, name):
        """As per the SAX handler, this method is where any work is
        done. You may want to override it, but probably not"""
        if name == 'node' or name == 'way' or name == 'relation':
            if self.selectElement():
                self.transformElement()
                self.modifyElement()
            self.clear()

    def endDocument(self):
#        print self.doc.toxml()
        self.doc.writexml(self.out, addindent='  ', newl = '\n', encoding = 'utf-8')

class PassThroughHandler(OSMHandler):
    def selectElement(self):
        return True

class MyHandler(OSMHandler):
    def selectElement(self):
        return self.attrs.get('id') == "55319624"

#parser = make_parser()
#parser.setContentHandler(MyHandler(sys.stdout))
#fname = sys.argv[1]
#out = sys.stdout
#fh = open(fname)
#parser.parse(fh)
