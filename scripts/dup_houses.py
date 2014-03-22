#!/usr/bin/env python

import sys
#from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from osmbot.pyxbot import OSMHandler
#import re
from osmbot.obj2xml import node2xml, way2xml

BOTNAME = "dup_house_bot"
VERSION = "0.1"
import quadpy
from quadpy.rectangle import Rectangle
quad = quadpy.Node(-180, -180, 180, 180, max_depth=19)
houses = []
nodes = {}


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

        if self.name in ("node"):
            xy = [float(x) for x in (self.attrs["lon"], self.attrs["lat"])]
            # print str(xy)
            nodes[self.attrs["id"]] = xy

        elif self.name in ("way"):
            if "building" in self.tags:
                bounds = self.bbox()
                rect = MyRect(*bounds)
                rect.data = Way(self)
                quad.insert(rect)

        for k in ("addr:housenumber",
                  "addr:postcode",
                  "addr:street",
                  "building",
                  "addr:city"
                  ):
            if not k in self.tags:
                return False

        if "landuse" in self.tags:
            return False

        if self.tags["building"] != "residential":
            return False

        if self.tags["addr:city"] != "Lawrence":
            return False

        if self.name not in ("node"):
            return False

        houses.append(Obj(self))

    def transformElement(self):
        """

        """
        # print str(self.__dict__)
        # self.deleteElement()

    def endDocument(self):

        for x in houses:
            # vals = []
            # for k in (
            #         "building",
            #         "addr:housenumber",
            #         "addr:postcode" ,
            #         "addr:street",
            #         "addr:city"):
            #     if k  in x.tags:
            #         vals.append(x.tags[k])
            xy = [float(v) for v in (x.attrs["lon"], x.attrs["lat"])]
            n = quad.get_children_under_point(xy[0], xy[1])
            if (n):
                if len(n) > 1:
                    raise Exception(n)
                n = n[0]
                # print  "|".join(vals)
                # print xy
                # print n
                for k in (
                        "building",
                        "addr:housenumber",
                        "addr:postcode",
                        "addr:street",
                        "addr:city"):
                    if k in x.tags:
                        n.data.tags[k] = x.tags[k]
                ele = self.doc.createElement('modify')
                ele.appendChild(way2xml(n.data))
                self.base.appendChild(ele)

                # call delete on node because it has been merged
                ele2 = self.doc.createElement('delete')
                ele2.appendChild(node2xml(x))
                self.base.appendChild(ele2)

        OSMHandler.endDocument(self)


parser = make_parser()
fname = sys.argv[1]
out = open('kate-output.osc', 'w')
fh = open(fname)
parser.setContentHandler(KateBot(out))
parser.parse(fh)


def test():
    import pprint
    for x in quad.get_children():
        print x, pprint.pformat(x.data.__dict__)

# self.deleteElement()
