#!/usr/bin/env python

import sys
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from pyxbot import OSMHandler

BOTNAME = "pyxbot"
VERSION = "0.1"

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
fname = sys.argv[1]
out = open('/home/serge/kate-output.osc','w')
fh = open(fname)
parser.setContentHandler(KateBot(out))
parser.parse(fh)
