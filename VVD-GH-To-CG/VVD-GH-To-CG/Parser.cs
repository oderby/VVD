using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using CSharpCommonGraph;
using GH_IO.Serialization;
using GH_IO.Types;
using System.Drawing;

namespace VVD_GH_To_CG
{
    static class Parser
    {

        //Actual constructor for use in the program
        public static CommonGraph CommonGraphFromGHFile(string file)
        {
            CommonGraph cg = new CommonGraph();


            //construct GH Archive object for XML Traversal
            GH_Archive archive = new GH_Archive();
            archive.ReadFromFile(file);

            //traverse GH file tree
            var rootNode = archive.GetRootNode;
            var definition = rootNode.FindChunk("Definition");
            var defObjects = definition.FindChunk("DefinitionObjects");
            int objCount = defObjects.GetInt32("ObjectCount");

            //for every object in the definition object list:
            for (int i = 0; i < objCount; i++)
            {
                var singleObjectChunk = defObjects.Chunks[i] as GH_Chunk;

                Guid typeGuid = singleObjectChunk.GetGuid("GUID");

                var container = singleObjectChunk.FindChunk("Container");

                var attributes = container.FindChunk("Attributes");

                var locPoint = attributes.GetDrawingPointF("Pivot");
             


                Guid instanceGuid = container.GetGuid("InstanceGuid");
                string name = singleObjectChunk.GetString("Name");

                IEnumerable<GH_IChunk> inputs;
                IEnumerable<GH_IChunk> outputs;
                
                //Components that implement variable parameters store their inputs/outputs one layer deeper.
                var parameterData = container.Chunks.Where<GH_IChunk>(C => C.Name == "ParameterData");
                bool hasParameterData = parameterData.Count() > 0;

                bool hasSourceCount = container.ItemExists("SourceCount");

                var paramChunks = container.Chunks;
                if (hasParameterData)
                {
                    paramChunks = parameterData.ToList()[0].Chunks;
                    inputs = paramChunks.Where(C => C.Name == "InputParam");
                    outputs = paramChunks.Where(C => C.Name == "OutputParam");
                }
                else
                {
                    
                   inputs = paramChunks.Where(C => C.Name == "param_input");
                    outputs = paramChunks.Where(C => C.Name == "param_output");
                }


             
              

             

                bool hasInputs = inputs.Count() > 0;
                bool hasOutputs = outputs.Count() > 0;
             
                bool isComponent = hasInputs || hasOutputs || hasParameterData;

                bool isActiveObject = isComponent || hasSourceCount;


                


                //Debugging 
                Console.WriteLine(name);
                Console.WriteLine("Is active object? " + isActiveObject.ToString());
                Console.WriteLine("Is Component? " + isComponent.ToString());


                if (!isActiveObject) continue;


                Node node = new Node();
                //type and instance
                node.Type = typeGuid.ToString();
                node.InstanceGuid = instanceGuid.ToString();
                node.Name = name;
                Position pos = new Position();
                pos.X = locPoint.X;
                pos.Y = locPoint.Y;
                node.Position = pos;

                //Metadata 
                MetaData md = new MetaData();
                md.Ignore = singleObjectChunk.Archive.Serialize_Xml();
                //TODO - REMOVE COMPONENTS OF XML THAT SHOULDN'T BE INSPECTED
                md.Inspect = singleObjectChunk.Archive.Serialize_Xml();
               node.Metadata = md; 

                List<Port> ports = new List<Port>();
                List<Edge> edges = new List<Edge>();
                if (isComponent) //if it's a component
                {
                    List<GH_IChunk> portChunks = new List<GH_IChunk>();
                    portChunks.AddRange(inputs);
                    portChunks.AddRange(outputs);
                  
                 
                    foreach (var portIChunk in portChunks) // for every port "chunk"
                    {
                        Port port = new Port();
                        GH_Chunk portChunk = portIChunk as GH_Chunk;
                        Guid portInstanceGuid = portChunk.GetGuid("InstanceGuid");
                        port.InstanceGuid = portInstanceGuid.ToString();
                        port.Name = portChunk.GetString("Name");
                        MetaData portMetadata = new MetaData();
                        portMetadata.Ignore = portChunk.Archive.Serialize_Xml();
                        port.MetaData = portMetadata; //REMEMBER TO UNCOMMENT
                        ports.Add(port);

                      

                        var sources = portChunk.Items.Where(item => item.Name == "Source");
                        Console.WriteLine("WE GOT THIS MANY SOURCES:" +sources.Count());
                        foreach(GH_Item item in sources){
                            Console.WriteLine("EDGE");
                             Edge edge = new Edge();
                            edge.DestGuid = portInstanceGuid.ToString();
                            edge.SrcGuid = item._guid.ToString();
                            edges.Add(edge);
                        }


                    }

                   
                  
                   
                } 
                else if(!isComponent && isActiveObject) //if it's a param
                {
                    Port port = new Port();
                    //wrapper for object - if it's a param, instance for virtual node and port are the same. 
                    Guid portInstanceGuid = instanceGuid;
                    port.InstanceGuid = instanceGuid.ToString();
                    port.Name = name;
                    ports.Add(port);
                }

                node.Ports = ports;
                cg.Edges.AddRange(edges);
                cg.Nodes.Add(node);
            }

            return cg;
        }
    }
}
