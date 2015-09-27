#!/usr/local/bin/python

import CommonGraphDiffer as cgd
import pygraphviz as pgv
import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("cg1")
    parser.add_argument("cg2")
    parser.add_argument("out")
    return parser.parse_args()

def main():
    args = parseArgs()
    CGA = cgd.CgxToObject(args.cg1)
    CGB = cgd.CgxToObject(args.cg2)
    ds = CGA.diff(CGB)

    G = pgv.AGraph()

    sameColor = 'grey'
    addedColor = 'green'
    removedColor = 'red'
    changedColor = 'orange'
    G.node_attr['fontsize'] =  4.0

    # add all nodes from CGA
    G.edge_attr['color'] = sameColor
    G.node_attr['color'] = sameColor
    for (nodeid, name) in CGA.getNodesAndNames():
        G.add_node(nodeid, color=sameColor, label=name, pin="true") # pos="4,4!")
        print nodeid
    for (src, dst) in CGA.getEdgePairs():
        print src,dst
        G.add_edge(src,dst)


       
    G.edge_attr['color'] = sameColor
    G.node_attr['color'] = sameColor

    for thisNodeChange in [change for change in ds.Changes if change.__class__.__name__ == "NodeChange"]:
        print thisNodeChange
        if(thisNodeChange.Status == "added"):
            G.add_node(cgd.Node.addFromChange(thisNodeChange).getLabel(), color=addedColor)
        if(thisNodeChange.Status == "removed"):
            G.get_node(thisNodeChange.InstanceGuid).attr['color']=removedColor
        if(thisNodeChange.Status == "changed"):
            G.get_node(thisNodeChange.InstanceGuid).attr['color']=changedColor

    for thisEdgeChange in [change for change in ds.Changes if change.__class__.__name__ == "EdgeChange"]:
        print thisEdgeChange
        if(thisEdgeChange.Status == "added"):
            G.add_edge(*cgd.Edge.addFromChange(thisEdgeChange).getEdgeLabelPairs(), color=addedColor)
        if(thisEdgeChange.Status == "removed"):
            thisEdge = [ed for ed in CGA.Edges if ed.InstanceGuid == thisEdgeChange.InstanceGuid][0]
            G.get_edge(*thisEdge.getEdgeLabelPairs()).attr['color']= removedColor

    print(G.string())
    G.layout() # layout with default (neato)
    G.draw(args.out)

if __name__ == "__main__":
    main()
