using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using CSharpCommonGraph;
using GH_IO.Serialization;

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
                Guid instanceGuid = container.GetGuid("InstanceGuid");
                string name = singleObjectChunk.GetString("Name");

                //Test if the object has sources (and is therefore an object of interest.)
                //TODO: improve this method
                bool isActiveObject = container.ItemExists("SourceCount");

                bool hasInputs = container.Chunks.Where(C => C.Name == "param_input").Count() > 0;
                bool hasOutputs = container.Chunks.Where(C => C.Name == "param_output").Count() > 0;
                bool isComponent = hasInputs || hasOutputs;

                Console.WriteLine(isComponent.ToString());
                Node node = new Node();
                node.Type = typeGuid.ToString();
                node.InstanceGuid = instanceGuid;





                cg.Nodes.Add(node);
            }

            return cg;
        }
    }
}
