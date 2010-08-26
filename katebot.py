#!/usr/bin/env python

import sys
from xml.sax.handler import ContentHandler
from xml.sax import make_parser

BOTNAME = "pyxbot"
VERSION = "0.1"

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
        if self.tags:
            self.out.write('<node %s >\n' %
                      ' '.join(['%s="%s"' % (x,y)
                                for x,y in self.attrs.items()]))
            for tag in self.tags:
                self.out.write(u'  <tag k="%s" v="%s" />\n' % (tag, self.tags[tag]))
            self.out.write('</node>\n')
        else:
            self.out.write('<node %s />\n' %
                      ' '.join(['%s="%s"' % (x,y)
                                for x,y in self.attrs.items()]))
    def _emit_way(self):
        "Output a way"
        self.out.write('<way %s >\n' % ' '.join(['%s="%s"' % (x, y)
                                            for x, y in self.attrs.items()]))
        if self.tags or self.nodes:
            for nodeid in self.nodes:
                self.out.write('  <nd ref="%s" />\n' % nodeid)
            for tag in self.tags:
                self.out.write('  <tag k="%s" v="%s" />\n'.decode()
                          % (tag, self.tags[tag]))
            self.out.write('</way>\n')
        else:
            self.out.write('<way %s />\n' %
                      ' '.join(['%s="%s"' % (x,y) for x,y in self.attrs]))

    def _emit_relation(self):
        "Output a relation"
        if self.members or self.tags:
            self.out.write('<relation %s >\n' %
                      ' '.join(['%s="%s"' % (x,y) for x,y in self.attrs]))
            for member in self.members:
                self.out.write('  <member %s />\n' %
                          ' '.join(['%s="%s"' % (x,y)
                                    for x,y in member.items()]))
            for tag in self.tags:
                self.out.write('  <tag k="%s" v="%s" />\n'.decode()
                          % (tag, self.tags[tag]))
            self.out.write('</relation>\n')
        else:
            self.out.write('<relation %s />\n' %
                      ' '.join(['%s="%s"' % (x,y)
                                for x,y in self.attrs.items()])) 
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
            self.attrs = dict(attrs.copy())
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

class KateBot(OSMHandler):
    def selectElement(self):
        if ( self.tags.get('source') == 'CCCM' and
             self.tags.get('attribute_source_type') == 'gisdataset' and
             self.tags.get('attribute_source_date') == '24-08-2010'):
            return True
        else:
            return False
    def transformElement(self):
        self.tags['camp'] = 'spontaneous'
        self.attrs['version'] = str(int(self.attrs.get('version')) + 1)
        del(self.attrs['uid'])
        del(self.attrs['user'])
        try:
            del(self.tags['website'])
        except KeyError:
            pass

parser = make_parser()
parser.setContentHandler(KateBot(sys.stdout))
fname = sys.argv[1]
out = sys.stdout
fh = open(fname)
parser.parse(fh)
