#!/usr/bin/env python

import sys
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from pyxbot import OSMHandler
import re

BOTNAME = "pyxbot"
VERSION = "0.1"
seen = {}

class KateBot(OSMHandler):
    def selectElement(self):
        if ( 'addr:street' in self.tags):
            st = self.tags.get('addr:street')
            up = st.capitalize()
            if (up != st):
            #    print up
                return True    
            else:
                return False

    def transformElement(self):

        st = self.tags.get('addr:street')
        up = st.lower().title()
        up.replace("Th","th")
        up = re.sub(r'^Us','US',up,0,re.IGNORECASE)
        up = re.sub(r'\sUs\s',' US ',up,0,re.IGNORECASE)

        up = re.sub(r'^\s+','',up)

        up = re.sub(r'^E\s','East ',up,0,re.IGNORECASE)
        up = re.sub(r'^W\s','West ',up,0,re.IGNORECASE)
        up = re.sub(r'^N\s','North ',up,0,re.IGNORECASE)
        up = re.sub(r'^S\s','South ',up,0,re.IGNORECASE)
        up = re.sub(r'^SE\s','Southeast ',up,0,re.IGNORECASE)
        up = re.sub(r'^SW\s','Southwest ',up,0,re.IGNORECASE)
        up = re.sub(r'^NE\s','Northeast ',up,0,re.IGNORECASE)
        up = re.sub(r'^NW\s','Northwest ',up)

        up = re.sub(r'^Ks','KS',up,0,re.IGNORECASE)
        up = re.sub(r'\sKs\s',' KS ',up,0,re.IGNORECASE)

        #if (up.startswith("")
        up = re.sub(r'(\d+)Th', r'\1th', up,0,re.IGNORECASE)
        up = re.sub(r'(\d+)Nd', r'\1nd', up,0,re.IGNORECASE)
        up = re.sub(r'(\d+)Rd', r'\1rd', up,0,re.IGNORECASE)
        up = re.sub(r'(\d+)St', r'\1st', up,0,re.IGNORECASE)
        if up not in seen:
            seen[up]=1
            print up

        self.tags['addr:street']=up.encode("ascii","replace")
#        self.attrs['version'] = str(int(self.attrs.get('version')) + 1)

parser = make_parser()
fname = sys.argv[1]
import codecs
out = codecs.open("katebot.osc", "wb", "utf-8")
fh  = codecs.open(fname, "rb", "utf-8")
parser.setContentHandler(KateBot(out))

parser.parse(fh)
