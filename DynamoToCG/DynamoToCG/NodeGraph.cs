using System;
using System.Collections.Generic;
using System.Linq;
using System.Xml;
//using Dynamo.Models;
//using Dynamo.Utilities;
using CSharpCommonGraph;

namespace DynamoToCG
{
    public class NodeGraph
    {
        public List<CSharpCommonGraph.Node> Nodes { get; private set; }
        public List<CSharpCommonGraph.Edge> Connectors { get; private set; }
  
        private NodeGraph() { }

        private static IEnumerable<CSharpCommonGraph.Node> LoadNodesFromXml(XmlDocument xmlDoc)
        {
            XmlNodeList elNodes = xmlDoc.GetElementsByTagName("Elements");
            if (elNodes.Count == 0)
                elNodes = xmlDoc.GetElementsByTagName("dynElements");
            XmlNode elNodesList = elNodes[0];
            return from XmlElement elNode in elNodesList.ChildNodes
                   select LoadNodeFromXml(elNode);
        }

        public static CommonGraph ToCommonCgraph(NodeGraph nodegraph)
        {
            var g = new CommonGraph();
            g.Nodes = nodegraph.Nodes;
            g.Edges = nodegraph.Connectors;
            return g;
        }

        /// <summary>
        ///     Creates and initializes a NodeModel from its Xml representation.
        /// </summary>
        /// <param name="elNode">XmlElement for a NodeModel.</param>
        /// <param name="context">The serialization context for initialization.</param>
        /// <param name="nodeFactory">A NodeFactory, to be used to create the node.</param>
        /// <returns></returns>
        public static CSharpCommonGraph.Node LoadNodeFromXml(
            XmlElement elNode)
        {
            var commonGraphNode = new CSharpCommonGraph.Node();
            commonGraphNode.InstanceGuid = elNode.GetAttribute("guid");

            //case 1 the node is a zero touch node
            if (elNode.GetAttribute("type") == "Dynamo.Nodes.DSFunction")
            {
                commonGraphNode.Type = elNode.GetAttribute("nickname");
            }
            else
            {
                //TODO handle other cases... like custom nodes and builtins?
                commonGraphNode.Type = elNode.GetAttribute("nickname");
            }

            commonGraphNode.Metadata.Inspect = elNode.ToString();
            //commonGraphNode.Ports = CreatPortsFromNode(commonGraphNode.InstanceGuid, edges);
            return commonGraphNode;
        }
     

        /// <summary>
        ///     Creates and initializes a ConnectorModel from its Xml representation.
        /// </summary>
        /// <param name="connEl">XmlElement for a ConnectorModel.</param>
        /// <param name="nodes">Dictionary to be used for looking up a NodeModel by it's Guid.</param>
        /// <returns>Returns the new instance of ConnectorModel loaded from XmlElement.</returns>
        public static CSharpCommonGraph.Edge LoadConnectorsAndAddPortsFromXml(XmlElement connEl,IDictionary<string, CSharpCommonGraph.Node> nodes)
        {
            var helper = new Dynamo.Utilities.XmlElementHelper(connEl);

            var guid = helper.ReadGuid("guid", Guid.NewGuid());
            var guidStart = helper.ReadGuid("start");
            var guidEnd = helper.ReadGuid("end");
            int startIndex = helper.ReadInteger("start_index");
            int endIndex = helper.ReadInteger("end_index");


             //find the elements to connect
            CSharpCommonGraph.Node start;
            if (nodes.TryGetValue(guidStart.ToString(), out start))
            {
                var startport = new CSharpCommonGraph.Port();
                startport.InstanceGuid = start.InstanceGuid.ToString()+"_"+startIndex.ToString();
                startport.MetaData.Inspect = "start";
                startport.Name = "a cool port";
                start.Ports.Add(startport);

                CSharpCommonGraph.Node end;
                if (nodes.TryGetValue(guidEnd.ToString(), out end))
                {


                    var endport = new CSharpCommonGraph.Port();
                    endport.InstanceGuid = end.InstanceGuid.ToString() + "_" + endIndex.ToString();
                    endport.MetaData.Inspect = "end";
                    endport.Name = "a cool port";
                    end.Ports.Add(endport);

                    var edge = new CSharpCommonGraph.Edge();
                    edge.SrcGuid = startport.InstanceGuid;
                    edge.DestGuid = endport.InstanceGuid;
                    return edge;
                }
            }

            return null;
          
            }

        private static IEnumerable<CSharpCommonGraph.Edge> LoadConnectorsFromXml(XmlDocument xmlDoc,IDictionary<string,CSharpCommonGraph.Node> nodes)
        {
            XmlNodeList cNodes = xmlDoc.GetElementsByTagName("Connectors");
            if (cNodes.Count == 0)
                cNodes = xmlDoc.GetElementsByTagName("dynConnectors");
            XmlNode cNodesList = cNodes[0];

            foreach (XmlElement connector in cNodesList.ChildNodes)
            {
                var c = LoadConnectorsAndAddPortsFromXml(connector, nodes);
                yield return c;
            }
        }

       
       

      
      
        /// <summary>
        ///     Loads NodeModels, ConnectorModels, and NoteModels from an XmlDocument.
        /// </summary>
        /// <param name="xmlDoc">An XmlDocument representing a serialized Dynamo workspace.</param>
        /// <param name="nodeFactory">A NodeFactory, used to load and instantiate nodes.</param>
        /// <param name="elementResolver"></param>
        /// <returns></returns>
        public static NodeGraph LoadGraphFromXml(XmlDocument xmlDoc)
        {
            //var elementResolver = LoadElementResolverFromXml(xmlDoc);
            var nodes = LoadNodesFromXml(xmlDoc).ToList();
            var connectors = LoadConnectorsFromXml(xmlDoc, nodes.ToDictionary(node => node.InstanceGuid)).ToList();

            return new NodeGraph { Nodes = nodes, Connectors = connectors};
        }

    }
}
