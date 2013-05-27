#!/usr/bin/env python

import sys
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from pyxbot import OSMHandler
import re

BOTNAME = "pyxbot"
VERSION = "0.1"

class KateBot(OSMHandler):
    def selectElement(self):
        if ( 'addr:street' in self.tags):
            st = self.tags.get('addr:street')
            up = st.capitalize
            if (up != st):
                print up
                return True    
            else:
                return False

    def transformElement(self):

        st = self.tags.get('addr:street')
        up = st.lower().title()
        up.replace("Th","th"        )
        up = re.sub(r'(\d+)Th', r'\1th', up)
        up = re.sub(r'(\d+)Rd', r'\1rd', up)
        up = re.sub(r'(\d+)St', r'\1st', up)

        self.tags['addr:street']=up
#        self.attrs['version'] = str(int(self.attrs.get('version')) + 1)

parser = make_parser()
fname = sys.argv[1]
out = open('kate-output.osc','w')
fh = open(fname)
parser.setContentHandler(KateBot(out))
parser.parse(fh)
