from xml.dom.minidom import Element


# We assume all the attributes are already strings
def tag2xml(k, v):
    """Takes a tag and returns it as XML"""
    ele = Element('tag')
    ele.setAttribute('k', k)
    ele.setAttribute('v', v)
    return ele


def node2xml(node):
    """Takes in a node object and returns an XML object for that node"""
    ele = Element('node')
    for k, v in node.attrs.items():
        ele.setAttribute(k, v)
    for k, v in node.tags.items():
        ele.appendChild(tag2xml(k, v))
    return ele


def way2xml(way):
    ele = Element('way')
    for k, v in way.attrs.items():
        ele.setAttribute(k, v)
    for ref in way.nodes:
        nd = Element('nd')
        nd.setAttribute('ref', ref)
        ele.appendChild(nd)
    for k, v in way.tags.items():
        ele.appendChild(tag2xml(k, v))
    return ele


def relation2xml(relation):
    ele = Element('relation')
    for k, v in relation.attrs.items():
        ele.setAttribute(k, v)
    for member in relation.members:
        ele = Element('member')
        for k, v in member.items():
            ele.setAttribute(k, v)
    for k, v in relation.tags.items():
        ele.appendChild(tag2xml(k, v))
    return ele
