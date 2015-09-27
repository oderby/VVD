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


def graphAddCGX(G, CGX, col='black'):
    # add all nodes from CGA
    G.edge_attr['color'] = col
    G.node_attr['color'] = col
    for (nodeid, name, position) in CGX.getNodesForGraphviz():
        print (nodeid, name, position) 
        G.add_node(nodeid, color=col, label=name, pin="true", pos=position + "!")
    for (src, dst) in CGX.getEdgePairs():
        print (src, dst)
        G.add_edge(src,dst)
    return G


def graphApplyDS(G, CGX,  ds, addedColor, removedColor, changedColor):
    for thisNodeChange in [change for change in ds.Changes if change.__class__.__name__ == "NodeChange"]:
        print thisNodeChange
        if(thisNodeChange.Status == "added"):
            (nodeid, name, position) = cgd.Node.getGraphVizRep(thisNodeChange)
            G.add_node(nodeid, color=addedColor, label=name, pin="true", pos=position + "!")
        if(thisNodeChange.Status == "removed"):
            G.get_node(thisNodeChange.InstanceGuid).attr['color']=removedColor
        if(thisNodeChange.Status == "changed"):
            G.get_node(thisNodeChange.InstanceGuid).attr['color']=changedColor

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

    G = pgv.AGraph(strict=False, directed=True)
    
    G.node_attr['fontsize'] =  2.0
    G.node_attr['shape'] = 'circle'

    G = graphAddCGX(G, CGA, 'grey')
   
    G = graphApplyDS(G, CGA, ds, addedColor='#319E8E', removedColor='#D13A82', changedColor='#FFDF4E')

    print G.string()
    G.layout(prog='neato') # layout with default (neato)
    G.draw(args.png)

if __name__ == "__main__":
    main()
