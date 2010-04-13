#!/usr/bin/env python

import sys
from xml.sax.handler import ContentHandler
from xml.sax import make_parser

class OSMHandler(ContentHandler):
    """This is a base OSMHandler class which sets up the XML parsing, etc.

    You will want to override the selectElement and transformElement
    functions"""
    def __init__(self):
        "Initiate the SAX state machine"
        self.clear()
    # These methods are quick n dirty. Very dirty.
    def _emit_node(self, out):
        "Output a node"
        if self.tags:
            out.write('<node %s >\n' %
                      ' '.join(['%s="%s"' % (x,y)
                                for x,y in self.attrs.items()]))
            for tag in self.tags:
                out.write(u'  <tag k="%s" v="%s" />\n' %
                          (tag, self.tags[tag]))
            out.write('</node>\n')
        else:
            out.write('<node %s />\n' %
                      ' '.join(['%s="%s"' % (x,y)
                                for x,y in self.attrs.items()]))
    def _emit_way(self, out):
        "Output a way"
        out.write('<way %s >\n' % ' '.join(['%s="%s"' % (x, y)
                                            for x, y in self.attrs.items()]))
        if self.tags or self.nodes:
            for nodeid in self.nodes:
                out.write('  <nd ref="%s" />\n' % nodeid)
            for tag in self.tags:
                out.write('  <tag k="%s" v="%s" />\n' % (tag, self.tags[tag]))
            out.write('</way>\n')
        else:
            out.write('<way %s />\n' %
                      ' '.join(['%s="%s"' % (x,y) for x,y in self.attrs]))

    def _emit_relation(self, out):
        "Output a relation"
        if self.members or self.tags:
            out.write('<relation %s >\n' %
                      ' '.join(['%s="%s"' % (x,y) for x,y in self.attrs]))
            for member in self.members:
                out.write('  <member %s />\n' %
                          ' '.join(['%s="%s"' % (x,y)
                                    for x,y in member.items()]))
            out.write('</relation>\n')
        else:
            out.write('<relation %s />\n' %
                      ' '.join(['%s="%s"' % (x,y)
                                for x,y in self.attrs.items()])) 
    def emit(self, out = sys.stdout):
        "Output the current element"
        if self.name == 'node':
            self._emit_node(out)
        elif self.name == 'way':
            self._emit_way(out)
        elif self.name == 'relation':
            self._emit_relation(out)

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
            self.nodes = attrs.get('ref')

    def selectElement(self):
        """Select whether or not we care about the OSM object (True or
        False). Override this function in your handler"""
        return False

    def transformElement(self):
        """Transform the element. Override this function in your
        handler"""
        pass
    def deleteElement(self):
        """Returns the string to delete the element.  Please use with
        caution!"""
        pass
    def endElement(self, name):
        """As per the SAX handler, this method is where any work is
        done. You may want to override it, but probably not"""
        if self.selectElement():
            self.transformElement()
            self.emit()
        self.clear()

class PassThroughHandler(OSMHandler):
    def selectElement(self):
        return True

parser = make_parser()
parser.setContentHandler(PassThroughHandler())
fname = sys.argv[1]
fh = open(fname)
parser.parse(fh)
