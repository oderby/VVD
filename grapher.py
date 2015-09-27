#!/usr/local/bin/python

import CommonGraphDiffer as cgd
import pygraphviz as pgv
import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("cg1", help="This is a .CGX (CommonGraph) file")
    parser.add_argument("ds", help="This is a .DSX (DiffSet) file")
    parser.add_argument("png", help="This is the output filename of a .png file")
    return parser.parse_args()


def graphAddCGX(G, CGX, sameColor ='gray', borderColor='black'):
    # add all nodes from CGA
    G.edge_attr['color'] = sameColor
    G.node_attr['color'] = borderColor
    G.node_attr['fillcolor'] = sameColor
    G.node_attr['style'] = 'filled'
    for (nodeid, name, position) in CGX.getNodesForGraphviz():
#        print (nodeid, name, position) 
        G.add_node(nodeid, color=borderColor, label=name, pin="true", pos=position + "!")
    for (src, dst) in CGX.getEdgePairs():
#        print (src, dst)
        G.add_edge(src,dst)
    return G


def graphApplyDS(G, CGX,  ds, borderColor, addedColor, removedColor, changedColor):
    G.node_attr['style'] = 'filled'
    for thisNodeChange in [change for change in ds.Changes if change.__class__.__name__ == "NodeChange"]:
        print thisNodeChange
        if(thisNodeChange.Status == "added"):
            (nodeid, name, position) = cgd.Node.getGraphVizRep(thisNodeChange)
	    G.node_attr['style'] = 'filled'
            G.add_node(nodeid, color=borderColor, fillcolor=addedColor, label=name, pin="true", pos=position + "!")
        if(thisNodeChange.Status == "removed"):
            G.get_node(thisNodeChange.InstanceGuid).attr['fillcolor']=removedColor
        if(thisNodeChange.Status == "changed"):
            G.get_node(thisNodeChange.InstanceGuid).attr['fillcolor']=changedColor

    for thisEdgeChange in [change for change in ds.Changes if change.__class__.__name__ == "EdgeChange"]:
        print thisEdgeChange
        if(thisEdgeChange.Status == "added"):
            # try to find parentEdge from CGX
            parentEdge = cgd.Edge.parentEdge(CGX, thisEdgeChange, ds)
            G.add_edge(*parentEdge, color=addedColor)
        if(thisEdgeChange.Status == "removed"):
            thisEdge = [ed for ed in CGX.Edges if ed.InstanceGuid == thisEdgeChange.InstanceGuid][0]
            G.get_edge(*cgd.Edge.parentEdge(CGX, thisEdge)).attr['color']= removedColor
    return G



def main():
    args = parseArgs()
    CGA = cgd.CgxToObject(args.cg1)
    ds =  cgd.XMLToDS(args.ds)

    G = pgv.AGraph('digraph foo {}')
 
    G.node_attr['fontsize'] =  10.0
    G.node_attr['shape'] = 'rectangle'

    print "## generating graph from", args.cg1, "and", args.ds

    borderColor = 'black'
    sameColor = '#DDDDDD'

    G = graphAddCGX(G, CGA, sameColor=sameColor, borderColor=borderColor)
   
    G = graphApplyDS(G, CGA, ds, borderColor=borderColor, addedColor='#00CC00', removedColor='#FF0066', changedColor='#FFFFAA')

    G.layout(prog='neato') # layout with default (neato)
    G.draw(args.png)

    print "## wrote", args.png

if __name__ == "__main__":
    main()
