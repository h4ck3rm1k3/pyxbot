#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from osmbot.pyxbot import OSMHandler
#import re
import quadpy
from osmbot.obj2xml import node2xml, way2xml

BOTNAME = "dup_house_bot"
VERSION = "0.1"

#print sys.modules['quadpy']
from quadpy.rectangle import Rectangle
quad = quadpy.Node(-180, -90, 180, 90)
houses = []
nodes = {}
used = {}


class Obj:
    def __init__(self, other):
        self.attrs = other.attrs
        self.tags = other.tags


class Way (Obj):

    def __init__(self, other):
        Obj.__init__(self, other)
        self.nodes = other.nodes


def bbox(nodes):
    bounds = [None, None, None, None]
    compare = (
        (0, 2),
        (1, 3)
    )
    for xy in nodes:
        for i, c in enumerate(compare):
            for n in c:
                if bounds[n] is None:
                    bounds[n] = xy[i]
            n = c[0]
            x = c[1]
            # min
            if bounds[n] > xy[i]:
                bounds[n] = xy[i]
            # max
            if bounds[x] < xy[i]:
                bounds[x] = xy[i]

    #print (nodes, bounds)
    return bounds


class MyRect (Rectangle):

    def __init__(self, a, b, c, d):
        Rectangle.__init__(self, a, b, c, d)
        self.data = None


class KateBot(OSMHandler):

    def __init__(self, out):
        OSMHandler.__init__(self, out)

    def bbox(self):
        return bbox([nodes[node] for node in self.nodes])

    def selectElement(self):

        if self.name == "node":
            xy = [float(x) for x in (self.attrs["lon"], self.attrs["lat"])]

            nodes[self.attrs["id"]] = xy

            for k in ("addr:housenumber",
                      "addr:postcode",
                      "addr:street",
                      "building",
                      "addr:city"
                      ):
                if not k in self.tags:
                    #print "missing k %s" % k
                    return False

            # skip over amenities, we want separate nodes for them,
            for k in ("amenity",
                      "landuse",
                      "shop",
                      "name", # skip over named items
                      ):
                if k in self.tags:
                    return False

            house = Obj(self)
            
            #print "adding", str(xy), (str(house.__dict__))
            houses.append(house)

        elif self.name in ("way"):
            if "building" in self.tags:
                bounds = self.bbox()
                rect = MyRect(*bounds)
                rect.data = Way(self)
                quad.insert(rect)
                return

    def endDocument(self):
        errors = 0

        for x in houses:

            xy = [float(v) for v in (x.attrs["lon"], x.attrs["lat"])]
            n = quad.get_children_under_point(xy[0], xy[1])
            if (n):
                if len(n) > 1:
                    house =  " ".join(x.tags[k] for k in (
                        "addr:street",
                        "addr:housenumber",
                    ))
                    #raise Exception("Overlapping Buildings:" + house + "\n"+ str(n) )
                    print ("Overlapping Buildings:" + house + "\n"+ str(n) )
                    errors = errors + 1
                n = n[0]

                # extract the way id and make sure we dont assign it twice
                wayid = n.data.attrs['id']
                if wayid not in used :
                    used[wayid]=1
                else:
                    vals = []
                    for k in (
                            "addr:street",
                            "addr:housenumber",
                    ):
                        vals.append(x.tags[k])
                    print ("each way can only be used once: " + " ".join(vals) + "\n"+ str(n.data.__dict__))
                    errors = errors + 1

                # copy the tags from the node to the way
                for k in x.tags:
                    n.data.tags[k] = x.tags[k]

                # modify the way
                ele = self.doc.createElement('modify')
                ele.appendChild(way2xml(n.data))
                self.base.appendChild(ele)

                # call delete on node because it has been merged
                ele2 = self.doc.createElement('delete')
                ele2.appendChild(node2xml(x))
                self.base.appendChild(ele2)
            else:
                #print ("Missing:" +str(x.__dict__))
                pass

        OSMHandler.endDocument(self)


parser = make_parser()
fname = sys.argv[1]
import codecs
out = codecs.open("merge-dup.osc", "wb", "utf-8")
fh  = codecs.open(fname, "rb", "utf-8")

parser.setContentHandler(KateBot(out))
parser.parse(fh)

def report():
    import pprint
    for x in quad.get_children():
        print x, pprint.pformat(x.data.__dict__)

    for x in houses:
        print x, pprint.pformat(x.__dict__)

# report()
