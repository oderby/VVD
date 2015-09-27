#!/usr/local/bin/python

from lxml import etree
from lxml.builder import E
import copy

# TODO: should use import xml.etree.ElementTree

def getMetaXML(metaData):
    if metaData is not None and metaData.find("Inspect") is not None:
        return E("MetaData", metaData.find("Inspect"))

def buildXML(tag, attributes, metaData):
    meta = getMetaXML(metaData)
    print "======================"
    print "building xml for ", tag
    print str(attributes)
    print etree.tostring(meta)
    if meta is not None:
        return E(tag, attributes, meta)
    return E(tag, attributes)

def statusToString(status):
    if status == "added":
        return "[+]"
    if status == "removed":
        return "[-]"
    if status == "changed":
        return "[/]"

class DiffSet(object):
    def __init__(self, MetaData):
        self.Changes = []
        self.MetaData = MetaData
    def addChange(self, Change):
        self.Changes.append(Change)
    def toXML(self):
        changes = [c.toXML() for c in self.Changes]
        meta = getMetaXML(self.MetaData)
        if meta is not None:
            changes.append(meta)
        return E("DiffSet", *changes)

class NodeChange(object):
    def __init__(self, Status, Node):
        self.Status = Status
        self.InstanceGuid = Node.InstanceGuid
        self.Type = Node.Type
        self.MetaData = Node.MetaData
    def toXML(self):
        attributes = {}
        attributes["Status"] = self.Status
        attributes["InstanceGuid"] = self.InstanceGuid
        if self.Status != "removed":
            attributes["Type"] = self.Type
        return buildXML("NodeChange", attributes, self.MetaData)

    def __repr__(self):
        return statusToString(self.Status) + ' Node (InstanceGuid: ' + self.InstanceGuid + ')'

class PortChange(object):
    def __init__(self, Status, Port):
        self.Status = Status
        self.InstanceGuid = Port.InstanceGuid
        self.ParentGuid = Port.ParentGuid
        self.MetaData = Port.MetaData
    def toXML(self):
        attributes = {}
        attributes["Status"] = self.Status
        attributes["InstanceGuid"] = self.InstanceGuid
        if self.Status != "removed":
            attributes["ParentGuid"] = self.ParentGuid
        return buildXML("PortChange", attributes, self.MetaData)
    def __repr__(self):
        return statusToString(self.Status) + ' Port (InstanceGuid: ' + self.InstanceGuid + ')'

class EdgeChange(object):
    def __init__(self, Status, Edge):
        self.Status = Status
        self.InstanceGuid = Edge.InstanceGuid
        self.SrcGuid = Edge.SrcGuid
        self.DstGuid = Edge.DstGuid
    def toXML(self):
        attributes = {}
        attributes["Status"] = self.Status
        attributes["InstanceGuid"] = self.InstanceGuid
        if self.Status != "removed":
            attributes["SrcGuid"] = self.SrcGuid
            attributes["DstGuid"] = self.DstGuid
        return E("Edgechange", attributes)
    def __repr__(self):
        return statusToString(self.Status) + ' Edge (InstanceGuid: ' + self.InstanceGuid + ')'



def booleanObjectLists(objType, selfObjs, otherObjs):

    selfIGs = set(x.InstanceGuid for x in selfObjs)  # All ids in list 1
    otherIGs = set(x.InstanceGuid for x in otherObjs)  # All ids in list 1

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
        if(objType == "edge"):
            self.Edges.append(obj)

    def removeObj(self, objType, obj):
        if(objType == "node"):
            objList = self.Nodes
        if(objType == "edge"):
            objList = self.Edges
        try:
            objList.remove(obj)
            return True
        except:
            return False
    def changeObj(self, objType, obj):
        if(objType == "node"):
            objList = self.Nodes
        if(objType == "edge"):
            objList = self.Edges
        try:
            for idx, thisN in enumerate(objList):
                if node == thisN:
                    objList[idx].MetaData = node.MetaData
            return True
        except:
            return False
    def getAllPorts(self):
        return [port for node in self.Nodes for port in node.Ports]

    def diff(self, other):
        #TODO: Compute diff for top-level MetaData field

        thisDiffSet = DiffSet(self.MetaData)

        (nodesRemoved, nodesAdded, nodesChanged, nodesSame) = booleanObjectLists("node", self.Nodes, other.Nodes)
        for thisNode in nodesRemoved:
            thisDiffSet.addChange(NodeChange("removed", thisNode))
        for thisNode in nodesAdded:
            thisDiffSet.addChange(NodeChange("added", thisNode))
        for thisNode in nodesChanged:
            thisDiffSet.addChange(NodeChange("changed", thisNode))

        (edgesRemoved, edgesAdded, edgesChanged, edgesSame) = booleanObjectLists("edge", self.Edges, other.Edges)
        for thisEdge in edgesRemoved:
            thisDiffSet.addChange(EdgeChange("removed", thisEdge))
        for thisEdge in edgesAdded:
            thisDiffSet.addChange(EdgeChange("added", thisEdge))

        (portsRemoved, portsAdded, portsChanged, portsSame) = booleanObjectLists("port", self.getAllPorts(), other.getAllPorts())

        for thisPort in portsRemoved:
            thisDiffSet.addChange(PortChange("removed", thisPort))
        for thisPort in portsAdded:
            thisDiffSet.addChange(PortChange("added", thisPort))
        for thisPort in portsChanged:
            thisDiffSet.addChange(PortChange("changed", thisPort))
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
                newCG.removeObj("node", Node.addFromChange(thisNodeChange))
            if(thisNodeChange.Status == "changed"):
                newCG.changeObj("node", Node.addFromChange(thisNodeChange))

        for thisPortChange in [change for change in diffSet.Changes if change.__class__.__name__ == "PortChange"]:
            print thisPortChange
            if(thisPortChange.Status == "added"):
                newCG.add("port", Port.addFromChange(thisPortChange))
            if(thisPortChange.Status == "removed"):
                newCG.removeObj("port", Port.addFromChange(thisPortChange))
            if(thisPortChange.Status == "changed"):
                newCG.changeObj("port", Port.addFromChange(thisPortChange))

        for thisEdgeChange in [change for change in diffSet.Changes if change.__class__.__name__ == "EdgeChange"]:
            print thisEdgeChange
            if(thisEdgeChange.Status == "added"):
                newCG.add("edge", Edge.addFromChange(thisEdgeChange))
            if(thisEdgeChange.Status == "removed"):
                newCG.removeObj("edge", Edge.addFromChange(thisEdgeChange))
            if(thisEdgeChange.Status == "changed"):
                newCG.changeObj("edge", Edge.addFromChange(thisEdgeChange))


        return newCG

class Node(object):
    def __init__(self, Type, InstanceGuid, MetaData):
        self.Type = Type
        self.InstanceGuid = InstanceGuid
        self.MetaData = MetaData
        self.Ports = []
    def __eq__(self, other):
        if self.InstanceGuid == other.InstanceGuid:
            return True
        else:
            return False
    @classmethod
    def addFromChange(cls, nodeChange):
        return cls(nodeChange.Type, nodeChange.InstanceGuid, nodeChange.MetaData)

    def __repr__(self):
        return '\n (#) Node (InstanceGuid: ' + self.InstanceGuid + ' Type: ' + self.Type + ') \n' +\
                '\n'.join([str(p) for p in self.Ports])
    def addPort(self, port):
        self.Ports.append(port)

class Port(object):
    def __init__(self, InstanceGuid, ParentGuid, MetaData):
        self.InstanceGuid = InstanceGuid
        self.ParentGuid = ParentGuid
        self.MetaData = MetaData
    def __repr__(self):
        return '\n    * Port (InstanceGuid: ' + self.InstanceGuid + ' ParentGuid: ' + self.ParentGuid + ')'
    @classmethod
    def addFromChange(cls, portChange):
        return cls(portChange.InstanceGuid, portChange.ParentGuid, portChange.MetaData)

class Edge(object):
    def __init__(self, SrcGuid, DstGuid):
        self.SrcGuid = SrcGuid
        self.DstGuid = DstGuid
        self.InstanceGuid = self.SrcGuid + "|" + self.DstGuid
    def __repr__(self):
        return '\n  == Edge (SrcGuid: ' + self.SrcGuid + ' DstGuid: ' + self.DstGuid + ')'
    @classmethod
    def addFromChange(cls, edgeChange):
        return cls(edgeChange.SrcGuid, edgeChange.DstGuid)



def recursive_dict(element):
    return element.tag, dict(map(recursive_dict, element)) or element.text

def CgxToObject(xmlfile):
    tree = etree.parse(xmlfile)
    root = tree.getroot()

    thisCG = CommonGraph(root.find("MetaData"))
    for xmlNode in root.findall(".//Node"):
        xmlNodeAsDict = recursive_dict(xmlNode)[1]
        thisNode = Node(xmlNode.get('Type'), xmlNode.get('InstanceGuid'), xmlNode.find('MetaData'))
        for xmlPort in xmlNode.findall(".//Port"):
            xmlPortAsDict = recursive_dict(xmlPort)[1]
            thisNode.addPort(Port(xmlPort.get('InstanceGuid'), thisNode.InstanceGuid, xmlPort.find('MetaData')))
        thisCG.add("node", thisNode)

    for xmlEdge in root.findall(".//Edge"):
        thisEdge = Edge(xmlEdge.get('SrcGuid'), xmlEdge.get('DstGuid'))
        thisCG.add("edge", thisEdge)
#	print thisCG.Nodes
#	print thisCG.Edges

    return thisCG

def DSToXML(diffSet, fileName):
    etree.ElementTree(diffSet.toXML()).write(fileName, standalone=True, pretty_print=True)

def main():
    CGA = CgxToObject("examples/simple_multiply_example.cgx")
    CGB = CgxToObject("examples/simple_multiply_example_b.cgx")
    ds = CGA.diff(CGB)


    DSToXML(ds, "foo.dsx")

    CGB2 = CGA.applyDiff(ds)

    print "========================="
#    print CGB2


if __name__ == "__main__":
    main()
