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
    # These methods are quick n dirty. Very dirty.
    def _emit_node(self, out):
        if self.tags:
            out.write('<node %s >\n' %
                      ' '.join(['%s="%s"' % (x,y) for x,y in self.attrs.items()]))
            for t in self.tags:
                out.write('  <tag k="%s" v="%s" />\n' % (t, self.tags[t]))
            out.write('</node>\n')
        else:
            out.write('<node %s />\n' %
                      ' '.join(['%s="%s"' % (x,y) for x,y in self.attrs.items()]))
    def _emit_way(self, out):
        out.write('<way %s >\n' % self._attr_str(self.attrs))
        if self.tags or self.nodes:
            for n in self.nodes:
                out.write('  <nd ref="%s" />\n' % n)
            for t in self.tags:
                out.write('  <tag k="%s" v="%s" />\n' % (t, self.tags[t]))
            out.write('</way>\n')
        else:
            out.write('<way %s />\n' %
                      ' '.join(['%s="%s"' % (x,y) for x,y in self.attrs]))
    def _emit_relation(self, out):
        if self.members or self.tags:
            out.write('<relation %s >\n' % self.attr_str(self.attrs))
            for m in self.members:
                out.write('  <member %s />\n' %
                           ' '.join(['%s="%s"' % (x,y) for x,y in m.items()]))
            out.write('</relation>\n')
        else:
            out.write('<relation %s />\n' %
                      ' '.join(['%s="%s"' % (x,y) for x,y in self.attrs.items()])) 
    def emit(self, out = sys.stdout):
        if self.name == 'node':
            self._emit_node(out)
        elif self.name == 'way':
            self._emit_way(out)
        elif self.name == 'relation':
            self._emit_relation(out)
    def clear(self):
        self.name = None
        self.tags = {}
        self.nodes = []
        self.members = []
        self.attrs = {}
    def startElement(self, name, attrs):
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
    def endElement(self, name):
        self.emit()
        self.clear()

parser = make_parser()
parser.setContentHandler(OSMHandler())
fname = sys.argv[1]
fh = open(fname)
parser.parse(fh)

