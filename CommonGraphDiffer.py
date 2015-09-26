#!/usr/local/bin/python

from lxml import etree
from lxml import objectify


class CommonGraph(object):
	def __init__(self):
		self.Nodes = []
		self.Edges = []
	def addNode(self, node):
		self.Nodes.append(node)
	def addEdge(self, edge):
		self.Edges.append(edge)

	def diff(self, other):

		## NODES 

		selfNodeIGs = set([node.InstanceGuid for node in self.Nodes])
		otherNodeIGs = set([node.InstanceGuid for node in other.Nodes])

		nodeRemovedGuids = list(selfNodeIGs - otherNodeIGs)
		nodeAddedGuids = list(otherNodeIGs - selfNodeIGs)
		nodeIntersectingGuids = list(otherNodeIGs.intersection(selfNodeIGs))

		nodeSameGuids = []
		nodeChangedGuids = []

		for thisGuid in nodeIntersectingGuids:
			selfNode = [node for node in self.Nodes if node.InstanceGuid == thisGuid][0] 
			otherNode = [node for node in other.Nodes if node.InstanceGuid == thisGuid][0]
			if(cmp(selfNode.MetaData, otherNode.MetaData) == 0):
				nodeSameGuids.append(thisGuid)
			else:
				nodeChangedGuids.append(thisGuid)
			
		print "removed node: ", nodeRemovedGuids
		print "added node: ", nodeAddedGuids
		print "same node: ", nodeSameGuids
		print "changed node: ", nodeChangedGuids

		print "---"

		## EDGES

		#IGP stands for Instance Guid Pairs
		selfEdgeIGPs = set([edge.pairStr() for edge in self.Edges])
		otherEdgeIGPs = set([edge.pairStr() for edge in other.Edges])

		edgeRemovedIGPs = list(selfEdgeIGPs - otherEdgeIGPs)
		edgeAddedIGPs = list(otherEdgeIGPs - selfEdgeIGPs)
		edgeSameIGPs = list(otherEdgeIGPs.intersection(selfEdgeIGPs))

			
		print "removed edge: ", edgeRemovedIGPs
		print "added edge: ", edgeAddedIGPs
		print "same edge: ", edgeSameIGPs

		

	


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
	def __repr__(self):
		return 'Edge (SrcGuid: ' + self.SrcGuid + ' DstGuid: ' + self.DstGuid + ')'
	def pairStr(self):
		return self.SrcGuid + "|" + self.DstGuid 
	

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

	print thisCG.Nodes
	print thisCG.Edges

	return thisCG

def main():
	CGA = CgxToObject("examples/simple_multiply_example.cgx")
	CGB = CgxToObject("examples/simple_multiply_example_b.cgx")
	CGA.diff(CGB)


if __name__ == "__main__":
	main()

