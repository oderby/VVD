#!/usr/local/bin/python

from lxml import etree
from lxml.builder import E
# TODO: should use import xml.etree.ElementTree 

def getMetaXML(change):
	return E("MetaData", E("Inspect", change.find("Inspect")))

class DiffSet(object):
	def __init__(self):
		self.Changes = []
				# TODO: This should track overall metadata changes...
	def addChange(self, Change):
		self.Changes.append(Change)
	def toXML(self):
		return E("DiffSet", getMetaXML(self.MetaData), *[c.toXML() for c in self.Changes])

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
			return E("NodeChange", attributes, getMetaXML(self.MetaData))
		return E("NodeChange", attributes)

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
			return E("NodeChange", attributes, getMetaXML(self.MetaData))
		return E("PortChange", attributes)

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
		return E("PortChange", attributes)




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
	def addNode(self, node):
		self.Nodes.append(node)
	def addEdge(self, edge):
		self.Edges.append(edge)
	def getAllPorts(self):
		return [port for node in self.Nodes for port in node.Ports]

	def diff(self, other):
		#TODO: Compute diff for top-level MetaData field

		thisDiffSet = DiffSet()

		(nodesRemoved, nodesAdded, nodesChanged, nodesSame) = booleanObjectLists("node", self.Nodes, other.Nodes)
		for thisNode in nodesRemoved:
			thisDiffSet.addChange(NodeChange("removed", thisNode))
		for thisNode in nodesAdded:
			thisDiffSet.addChange(NodeChange("added", thisNode))
		for thisNode in nodesChanged:
			thisDiffSet.addChange(NodeChange("changed", thisNode))

		print "NODES"
		print "nodesRemoved: ", nodesRemoved
		print "nodesAdded: ", nodesAdded
		print "nodesChanged: ", nodesChanged

		(edgesRemoved, edgesAdded, edgesChanged, edgesSame) = booleanObjectLists("edge", self.Edges, other.Edges)
		for thisEdge in edgesRemoved:
			thisDiffSet.addChange(EdgeChange("removed", thisEdge))
		for thisEdge in edgesAdded:
			thisDiffSet.addChange(EdgeChange("added", thisEdge))

		print "EDGES"
		print "edgesRemoved: ", edgesRemoved
		print "edgesAdded: ", edgesAdded

		(portsRemoved, portsAdded, portsChanged, portsSame) = booleanObjectLists("port", self.getAllPorts(), other.getAllPorts())
		print "PORTS"
		print "portsRemoved: ", portsRemoved
		print "portsAdded: ", portsAdded
		print "portsChanged: ", portsChanged

		for thisPort in portsRemoved:
			thisDiffSet.addChange(PortChange("removed", thisPort))
		for thisPort in portsAdded:
			thisDiffSet.addChange(PortChange("added", thisPort))
		for thisPort in portsChanged:
			thisDiffSet.addChange(PortChange("changed", thisPort))


class Node(object):
	def __init__(self, Type, InstanceGuid, MetaData):
		self.Type = Type
		self.InstanceGuid = InstanceGuid
		self.MetaData = MetaData
		self.Ports = []
	def __repr__(self):
		return '\n=== Node (InstanceGuid: ' + self.InstanceGuid + ' Type: ' + self.Type + ') \n' +\
				'\n'.join([str(p) for p in self.Ports])
	def addPort(self, port):
		self.Ports.append(port)

class Port(object):
	def __init__(self, InstanceGuid, ParentGuid, MetaData):
		self.InstanceGuid = InstanceGuid
		self.ParentGuid = ParentGuid
		self.MetaData = MetaData
	def __repr__(self):
		return 'Port (InstanceGuid: ' + self.InstanceGuid + ' ParentGuid: ' + self.ParentGuid + ')'

class Edge(object):
	def __init__(self, SrcGuid, DstGuid):
		self.SrcGuid = SrcGuid
		self.DstGuid = DstGuid
		self.InstanceGuid = self.SrcGuid + "|" + self.DstGuid
	def __repr__(self):
		return 'Edge (SrcGuid: ' + self.SrcGuid + ' DstGuid: ' + self.DstGuid + ')'


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
		thisCG.addNode(thisNode)

	for xmlEdge in root.findall(".//Edge"):
		thisEdge = Edge(xmlEdge.get('SrcGuid'), xmlEdge.get('DstGuid'))
		thisCG.addEdge(thisEdge)
#	print thisCG.Nodes
#	print thisCG.Edges

	return thisCG

def DSToXML(diffSet, fileName):
	etree.ElementTree(diffSet.toXML()).write(fileName)

def main():
	CGA = CgxToObject("examples/simple_multiply_example.cgx")
	CGB = CgxToObject("examples/simple_multiply_example_b.cgx")
	CGA.diff(CGB)


if __name__ == "__main__":
	main()
