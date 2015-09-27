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
		self.ParentGuid = Port.ParentGuid
		self.MetaData = Port.MetaData

class EdgeChange(object):
	def __init__(self, Status, Edge):
		self.Status = Status
		self.InstanceGuid = Edge.InstanceGuid
		self.SrcGuid = Edge.SrcGuid
		self.DstGuid = Edge.DstGuid


def booleanObjectLists(selfObjs, otherObjs):

	selfIGs = set(x.InstanceGuid for x in selfObjs)  # All ids in list 1
	otherIGs = set(x.InstanceGuid for x in selfObjs)  # All ids in list 1

	objsRemoved = [item for item in selfObjs if item.InstanceGuid not in otherIGs] 
	objsAdded = [item for item in otherObjs if item.InstanceGuid not in selfIGs] 
	objsIntersection = [item for item in otherObjs if item.InstanceGuid in selfIGs] 

	return (objsRemoved, objsAdded, objsIntersection)


class CommonGraph(object):
	def __init__(self):
		self.Nodes = []
		self.Edges = []
	def addNode(self, node):
		self.Nodes.append(node)
	def addEdge(self, edge):
		self.Edges.append(edge)

	def diff(self, other):

		thisDiffSet = DiffSet()

		## NODES 


		# compare self and other nodes, and get three different sets
		# using those three different sets, write node changes
		# but - if the nodes are the same, scan for ports
		

		(nodesRemoved, nodesAdded, nodesIntersecting) = booleanObjectLists(self.Nodes, other.Nodes)

		print nodesRemoved
		for thisNode in nodesRemoved:
			print thisNode
			thisDiffSet.addChange(NodeChange("removed", thisNode))
		for thisNode in nodesAdded:
			print thisNode
			thisDiffSet.addChange(NodeChange("added", thisNode))
		for thisNode in nodesIntersecting:
			print thisNode
		print thisDiffSet.Changes
		"""
		nodeSameGuids = []
		nodeChangedGuids = []

		# if the node is intersecting, node is either same or modified
		for thisGuid in nodeIntersectingGuids:
			selfNode = [node for node in self.Nodes if node.InstanceGuid == thisGuid][0] 
			otherNode = [node for node in other.Nodes if node.InstanceGuid == thisGuid][0]

			(portRemovedGuids, portAddedGuids, portSameGuids) = booleanObjectLists([obj.InstanceGuid for obj in selfNode.Ports], [obj.InstanceGuid for obj in otherNode.Ports])

			print "---PORTS--"
			print "removed ports" , portRemovedGuids 
			print "added porst", portAddedGuids  
			print "same ports", portSameGuids 


			#metadata is different
			if(cmp(selfNode.MetaData['Inspect'], otherNode.MetaData['Inspect']) == 0):
				nodeSameGuids.append(thisGuid)
			else:
				nodeChangedGuids.append(thisGuid)
			
		print "---NODES--"
		print "removed node: ", nodeRemovedGuids
		print "added node: ", nodeAddedGuids
		print "same node: ", nodeSameGuids
		print "changed node: ", nodeChangedGuids

		## EDGES

		#IGP stands for Instance Guid Pairs
		(edgeRemovedIGPs, edgeAddedIGPs, edgeSameIGPs) = booleanObjectLists([edge.InstanceGuid for edge in self.Edges], [edge.InstanceGuid for edge in other.Edges])

		print "---EDGES--"
		print "removed edge: ", edgeRemovedIGPs
		print "added edge: ", edgeAddedIGPs
		print "same edge: ", edgeSameIGPs
		"""

		

	


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

