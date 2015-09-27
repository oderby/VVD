#!/usr/local/bin/python

from lxml import etree


class DiffSet(object):
	def __init__(self):
		self.Changes = []
	def addChange(self, Change):
		self.Changes.append(Change)

class NodeChange(object):
	def __init__(self, Status, Node):
		self.Status = Status
		self.InstanceGuid = Node.InstanceGuid
		self.Type = Node.Type
		self.MetaData = Node.MetaData

class PortChange(object):
	def __init__(self, Status, Port):
		self.Status = Status
		self.InstanceGuid = Port.InstanceGuid
#		self.ParentGuid = Port.ParentGuid
		self.MetaData = Port.MetaData

class EdgeChange(object):
	def __init__(self, Status, Edge):
		self.Status = Status
		self.InstanceGuid = Edge.InstanceGuid
		self.SrcGuid = Edge.SrcGuid
		self.DstGuid = Edge.DstGuid


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
	def __init__(self):
		self.Nodes = []
		self.Edges = []
	def addNode(self, node):
		self.Nodes.append(node)
	def addEdge(self, edge):
		self.Edges.append(edge)
	def getAllPorts(self):
		return [port for node in self.Nodes for port in node.Ports]

	def diff(self, other):

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
	def __init__(self, InstanceGuid, MetaData):
		self.InstanceGuid = InstanceGuid
		self.MetaData = MetaData
	def __repr__(self):
		return 'Port (InstanceGuid: ' + self.InstanceGuid + ')'

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

	thisCG = CommonGraph()
	for xmlNode in root.findall(".//Node"):
		xmlNodeAsDict = recursive_dict(xmlNode)[1]
		thisNode = Node(xmlNode.get('Type'), xmlNode.get('InstanceGuid'), xmlNodeAsDict['MetaData'])
		for xmlPort in xmlNode.findall(".//Port"):
			xmlPortAsDict = recursive_dict(xmlPort)[1]
			thisNode.addPort(Port(xmlPort.get('InstanceGuid'), xmlPortAsDict['MetaData']))
		thisCG.addNode(thisNode)

	for xmlEdge in root.findall(".//Edge"):
		thisEdge = Edge(xmlEdge.get('SrcGuid'), xmlEdge.get('DstGuid'))
		thisCG.addEdge(thisEdge)

#	print thisCG.Nodes
#	print thisCG.Edges

	return thisCG

def main():
	CGA = CgxToObject("examples/simple_multiply_example.cgx")
	CGB = CgxToObject("examples/simple_multiply_example_b.cgx")
	CGA.diff(CGB)


if __name__ == "__main__":
	main()

