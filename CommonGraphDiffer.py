#!/usr/local/bin/python

import xml.etree.ElementTree as etree
E = etree.Element
import copy
from xml.dom import minidom


def getMetaXML(metaData):
    if metaData is not None and metaData.find("Inspect") is not None:
        e = E("MetaData")
        e.append(metaData.find("Inspect"))
        return e

def buildXML(tag, attributes, metaData):
    meta = getMetaXML(metaData)
    if meta is not None:
        e = E(tag, attributes)
        e.append(meta)
        return e
    return E(tag, attributes)

def statusToString(status):
    if status == "added":
        return "[+]"
    if status == "removed":
        return "[-]"
    if status == "changed":
        return "[/]"

class DiffSet(object):
    def __init__(self, MetaData=None):
        self.Changes = []
        self.MetaData = MetaData
    def addChange(self, Change):
        self.Changes.append(Change)
    def toXML(self):
        changes = [c.toXML() for c in self.Changes]
        meta = getMetaXML(self.MetaData)
        if meta is not None:
            changes.append(meta)
        e = E("DiffSet")
        e.extend(changes)
        return e
    def __repr__(self):
        return '\n'.join([str(c) for c in self.Changes])

class NodeChange(object):
    def __init__(self, Status, InstanceGuid, Location=None, Type=None, MetaData=None):
        self.Status = Status
        self.InstanceGuid = InstanceGuid
        self.Location = Location
        self.Type = Type
        self.MetaData = MetaData
    def toXML(self):
        attributes = {}
        attributes["Status"] = self.Status
        attributes["InstanceGuid"] = self.InstanceGuid
        if self.Status != "removed":
            attributes["Type"] = self.Type
        e = buildXML("NodeChange", attributes, self.MetaData)
        if self.Location is not None:
            e.append(self.Location)
        return e

    def __repr__(self):
        return statusToString(self.Status) + ' Node (InstanceGuid: ' + self.InstanceGuid + ')'

class PortChange(object):
    def __init__(self, Status, InstanceGuid, ParentGuid=None, MetaData=None):
        self.Status = Status
        self.InstanceGuid = InstanceGuid
        self.ParentGuid = ParentGuid
        self.MetaData = MetaData
    def toXML(self):
        attributes = {}
        attributes["Status"] = self.Status
        attributes["InstanceGuid"] = self.InstanceGuid
        attributes["ParentGuid"] = self.ParentGuid
        return buildXML("PortChange", attributes, self.MetaData)
    def __repr__(self):
        return statusToString(self.Status) + ' Port (InstanceGuid: ' + self.InstanceGuid + ')'

class EdgeChange(object):
    def __init__(self, Status, InstanceGuid, SrcGuid=None, DstGuid=None):
        self.Status = Status
        self.InstanceGuid = InstanceGuid
        self.SrcGuid = SrcGuid
        self.DstGuid = DstGuid
    def toXML(self):
        attributes = {}
        attributes["Status"] = self.Status
        attributes["InstanceGuid"] = self.InstanceGuid
        if self.Status != "removed":
            attributes["SrcGuid"] = self.SrcGuid
            attributes["DstGuid"] = self.DstGuid
        return E("EdgeChange", attributes)
    def __repr__(self):
        return statusToString(self.Status) + ' Edge (InstanceGuid: ' + self.InstanceGuid + ')'



def booleanObjectLists(objType, selfObjs, otherObjs):

    selfIGs = set(x.InstanceGuid for x in selfObjs)  # All ids in list 1
    otherIGs = set(x.InstanceGuid for x in otherObjs)  # All ids in list 2

    objsRemoved = [item for item in selfObjs if item.InstanceGuid not in otherIGs]
    objsAdded = [item for item in otherObjs if item.InstanceGuid not in selfIGs]
    objsIntersection = [item for item in selfObjs if item.InstanceGuid in otherIGs]

    objsSame = []
    objsChanged = []

    if objType == "node" or objType == "port":
        for selfObj in objsIntersection:
            otherObj = [obj for obj in otherObjs if obj.InstanceGuid == selfObj.InstanceGuid][0]
            if( cmp(otherObj.MetaData, selfObj.MetaData) == 0): #it's the samE!
                objsSame.append(otherObj)
            else:
                objsChanged.append(otherObj)

    if objType == "edge":
        objsSame = objsIntersection

    return (objsRemoved, objsAdded, objsChanged, objsSame)


class CommonGraph(object):
    def __init__(self, MetaData):
        self.MetaData = MetaData
        self.Nodes = []
        self.Edges = []
    def __repr__(self):
        return repr(self.Nodes) + repr(self.Edges)

    def add(self, objType, obj):
        if(objType == "node"):
            self.Nodes.append(obj)
            return True
        if(objType == "edge"):
            self.Edges.append(obj)
            return True
        if(objType == "port"):
            parentNode = [n for n in self.Nodes if n.InstanceGuid == obj.ParentGuid][0]
            parentNode.addPort(obj)
            return True

    def removeObj(self, objType, objGuid, objParentGuid=None):
        if(objType == "node"):
            objList = self.Nodes
        if(objType == "edge"):
            objList = self.Edges
        if(objType == "port"):
            try:
                parentNode = [node for node in self.Nodes if node.InstanceGuid == objParentGuid][0]
                objList = parentNode.Ports
            except Exception, e:
                # this sometimes doesn't work because parentNode was already deleted - and that's okay!
                return True
        try:
            objList.remove([o for o in objList if o.InstanceGuid == objGuid][0])
        except:
            return False
        return True

    def changeObj(self, objType, obj, objParentGuid = None):
        if(objType == "node"):
            objList = self.Nodes
        if(objType == "edge"):
            objList = self.Edges
        if(objType == "port"):
            try:
                parentNode = [node for node in self.Nodes if node.InstanceGuid == objParentGuid][0]
                objList = parentNode.Ports
            except Exception, e:
                # if this doesn't work, this is bad
                return False
        try:
            for idx, thisN in enumerate(objList):
                if obj == thisN:
                    objList[idx].MetaData = obj.MetaData
            return True
        except Exception, e:
            return False

    def getAllPorts(self):
        return [port for node in self.Nodes for port in node.Ports]

    def diff(self, other):
        # If the metadata changed, include the other's metadata
        if cmp(recursive_dict(self.MetaData), recursive_dict(other.MetaData)) !=0:
            thisDiffSet = DiffSet(other.MetaData)
        else:
            thisDiffSet = DiffSet()

        (nodesRemoved, nodesAdded, nodesChanged, nodesSame) = booleanObjectLists("node", self.Nodes, other.Nodes)
        for thisNode in nodesRemoved:
            thisDiffSet.addChange(NodeChange("removed", thisNode.InstanceGuid))
        for thisNode in nodesAdded:
            thisDiffSet.addChange(NodeChange("added", thisNode.InstanceGuid, thisNode.Location, thisNode.Type, thisNode.MetaData))
        for thisNode in nodesChanged:
            thisDiffSet.addChange(NodeChange("changed", thisNode.InstanceGuid, thisNode.Location, thisNode.Type, thisNode.MetaData))

        (edgesRemoved, edgesAdded, edgesChanged, edgesSame) = booleanObjectLists("edge", self.Edges, other.Edges)
        for thisEdge in edgesRemoved:
            thisDiffSet.addChange(EdgeChange("removed", thisEdge.InstanceGuid))
        for thisEdge in edgesAdded:
            thisDiffSet.addChange(EdgeChange("added", thisEdge.InstanceGuid, thisEdge.SrcGuid, thisEdge.DstGuid))

        (portsRemoved, portsAdded, portsChanged, portsSame) = booleanObjectLists("port", self.getAllPorts(), other.getAllPorts())

        for thisPort in portsRemoved:
            thisDiffSet.addChange(PortChange("removed", thisPort.InstanceGuid, thisPort.ParentGuid))
        for thisPort in portsAdded:
            thisDiffSet.addChange(PortChange("added", thisPort.InstanceGuid, thisPort.ParentGuid, thisPort.MetaData))
        for thisPort in portsChanged:
            thisDiffSet.addChange(PortChange("changed", thisPort.InstanceGuid, thisPort.ParentGuid, thisPort.MetaData))
        return thisDiffSet

    def applyDiff(self, diffSet):
        # order is important: iterate over node changes, then port changes, then edge changes

        """
        # order is important: iterate over node changes, then port changes, then edge changes
        node:
            if change is an addition then turn a change into a node and add the node.
            if change is an removal then TRY removing node  (otherwise failure)
            if change is an modification then TRY replace old node metadata with new metadata (otherwise failure)
        port:
            if change is an addition then turn a change into a port and add the port.
            if change is an removal then TRY removing port  (otherwise failure)
            if change is an modification then TRY replace old port metadata with new metadata (otherwise failure)
        edge:
            if change is an addition then turn a change into a edge and add the edge.
            if change is an removal then TRY removing edge  (otherwise failure)
        """

        newCG = copy.deepcopy(self)

        for thisNodeChange in [change for change in diffSet.Changes if change.__class__.__name__ == "NodeChange"]:
            print thisNodeChange
            if(thisNodeChange.Status == "added"):
                newCG.add("node", Node.addFromChange(thisNodeChange))
            if(thisNodeChange.Status == "removed"):
                newCG.removeObj("node", thisNodeChange.InstanceGuid)
            if(thisNodeChange.Status == "changed"):
                newCG.changeObj("node", Node.addFromChange(thisNodeChange))

        for thisPortChange in [change for change in diffSet.Changes if change.__class__.__name__ == "PortChange"]:
            print thisPortChange
            if(thisPortChange.Status == "added"):
                newCG.add("port", Port.addFromChange(thisPortChange))
            if(thisPortChange.Status == "removed"):
                newCG.removeObj("port", thisPortChange.InstanceGuid, objParentGuid = thisPortChange.ParentGuid)
            if(thisPortChange.Status == "changed"):
                newCG.changeObj("port", Port.addFromChange(thisPortChange), objParentGuid = thisPortChange.ParentGuid)

        for thisEdgeChange in [change for change in diffSet.Changes if change.__class__.__name__ == "EdgeChange"]:
            print thisEdgeChange
            if(thisEdgeChange.Status == "added"):
                newCG.add("edge", Edge.addFromChange(thisEdgeChange))
            if(thisEdgeChange.Status == "removed"):
                newCG.removeObj("edge", thisEdgeChange.InstanceGuid)

        return newCG

class Node(object):
    def __init__(self, Type, InstanceGuid, Location, MetaData):
        self.Type = Type
        self.InstanceGuid = InstanceGuid
        self.Location = Location
        self.MetaData = MetaData
        self.Ports = []
    def __eq__(self, other):
        if self.InstanceGuid == other.InstanceGuid:
            return True
        else:
            return False
    @classmethod
    def addFromChange(cls, nodeChange):
        return cls(nodeChange.Type, nodeChange.Location, nodeChange.InstanceGuid, nodeChange.MetaData)

    def __repr__(self):
        s = '\n (#) Node (InstanceGuid: ' + self.InstanceGuid + ' Type: ' + self.Type
        if self.Location is not None:
            s += 'Location:' + etree.tostring(self.Location)
        if self.MetaData is not None:
            s += ' MetaData: ' + etree.tostring(self.MetaData)
        s += ' ) \n' + '\n'.join([str(p) for p in self.Ports])
        return s

    def addPort(self, port):
        self.Ports.append(port)

class Port(object):
    def __init__(self, InstanceGuid, ParentGuid, MetaData):
        self.InstanceGuid = InstanceGuid
        self.ParentGuid = ParentGuid
        self.MetaData = MetaData
    def __eq__(self, other):
        if self.InstanceGuid == other.InstanceGuid:
            return True
        else:
            return False
    def __repr__(self):
        return '\n    * Port (InstanceGuid: ' + self.InstanceGuid + ' ParentGuid: ' + self.ParentGuid + ' MetaData: ' + etree.tostring(self.MetaData) + ' )'
    @classmethod
    def addFromChange(cls, portChange):
        return cls(portChange.InstanceGuid, portChange.ParentGuid, portChange.MetaData)

class Edge(object):
    def __init__(self, SrcGuid, DstGuid):
        self.SrcGuid = SrcGuid
        self.DstGuid = DstGuid
        self.InstanceGuid = self.SrcGuid + "|" + self.DstGuid
    def __eq__(self, other):
        if self.InstanceGuid == other.InstanceGuid:
            return True
        else:
            return False
    def __repr__(self):
        return '\n  == Edge (SrcGuid: ' + self.SrcGuid + ' DstGuid: ' + self.DstGuid + ')'
    @classmethod
    def addFromChange(cls, edgeChange):
        return cls(edgeChange.SrcGuid, edgeChange.DstGuid)



def recursive_dict(element):
    if element is None:
        return {}
    return element.tag, dict(map(recursive_dict, element)) or element.text

def CgxToObject(xmlfile):
    tree = etree.parse(xmlfile)
    root = tree.getroot()

    thisCG = CommonGraph(root.find("MetaData"))
    for xmlNode in root.findall(".//Node"):
        xmlNodeAsDict = recursive_dict(xmlNode)[1]
        thisNode = Node(xmlNode.get('Type'), xmlNode.get('InstanceGuid'), xmlNode.find('Location'), xmlNode.find('MetaData'))
        for xmlPort in xmlNode.findall(".//Port"):
            xmlPortAsDict = recursive_dict(xmlPort)[1]
            thisNode.addPort(Port(xmlPort.get('InstanceGuid'), thisNode.InstanceGuid, xmlPort.find('MetaData')))
        thisCG.add("node", thisNode)

    for xmlEdge in root.findall(".//Edge"):
        thisEdge = Edge(xmlEdge.get('SrcGuid'), xmlEdge.get('DstGuid'))
        thisCG.add("edge", thisEdge)

    return thisCG

def prettify(elem):
    # Return a pretty-printed XML string for the Element.
    rough_string = etree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def DSToXML(diffSet, fileName):
    with open(fileName, "w") as fp:
        fp.write( prettify(diffSet.toXML()))

def XMLToDS(fileName):
    tree = etree.parse(fileName)
    root = tree.getroot()
    #print root.findall("*")
    xmlChanges = [e for e in root.findall("*") if e.tag.find("Change")>=0]

    thisDiffSet = DiffSet(root.find("MetaData"))
    for xmlChange in xmlChanges:
        status = xmlChange.get("Status")
        if xmlChange.tag == "NodeChange":
            change = NodeChange(status,xmlChange.get("InstanceGuid"), xmlChange.find("Location"), xmlChange.get("Type"), xmlChange.find("MetaData"))
        elif xmlChange.tag == "PortChange":
            change = PortChange(status, xmlChange.get("InstanceGuid"), xmlChange.get("ParentGuid"), xmlChange.find("MetaData"))
        elif xmlChange.tag == "EdgeChange":
            change = EdgeChange(status, xmlChange.get("InstanceGuid"), xmlChange.get("SrcGuid"), xmlChange.get("DstGuid"))
        else:
            print "!!!!!unknown tag", xmlChange.tag
        thisDiffSet.addChange(change)
    return thisDiffSet

def main():
    CGA = CgxToObject("examples/simple_multiply_example.cgx")

    CGB = CgxToObject("examples/simple_multiply_example_b.cgx")
    ds = CGA.diff(CGB)
    DSToXML(ds, "foo.dsx")
    ds2 = XMLToDS("foo.dsx")
    DSToXML(ds2, "foo2.dsx")

    print "========================="
    CGB2 = CGA.applyDiff(ds)
    print "========================="
    CGB3 = CGA.applyDiff(ds2)

    print "=CGA========================"
    print CGA
    print "=CGB========================"
    print CGB
    print "=CGB2========================"
    print CGB2
    print "=CGB3========================"
    print CGB3
    print "========================="

main()
