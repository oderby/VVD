using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using GH_IO;
using GH_IO.Serialization;
using GH_IO.Types;
using CSharpCommonGraph;
using System.Reflection;
using System.Xml;
using System.IO;
using System.Xml.Serialization;
using System.Xml.Linq;



namespace VVD_GH_To_CG
{
    public class GH_FileComposer
    {
        CommonGraph graph;
        GH_Archive archive;
        XDocument doc;
        public GH_FileComposer(CommonGraph cg)
        {
            graph = cg;
            archive = new GH_Archive();

            doc = XDocument.Parse(graph.MetaData.Ignore);

            File.WriteAllText(@"C:\Users\aheumann\Desktop\xml out test.txt", graph.MetaData.Ignore);
           

            ConstructGH2();
        }

        private void ConstructGH()
        {
            //set up the base file
            archive.Deserialize_Xml(graph.MetaData.Ignore);
            var rootNode = archive.GetRootNode;
            var Definition = rootNode.FindChunk("Definition") as GH_Chunk;
            var DefinitionObjects = Definition.FindChunk("DefinitionObjects") as GH_Chunk;
            // Definition.RemoveChunk("DefinitionObjects");

            ClearChunks(DefinitionObjects);
            foreach (Node n in graph.Nodes)
            {
                string objectXML = n.Metadata.Ignore;
              // archive.ExtractObject()
              
            

            }



        }


        XElement findChunk(XElement node, string name)
        {
            var Chunks = node.Elements().Where(elem => elem.Name == "chunks").First();
            var theElement = Chunks.Elements().Where(elem => elem.FirstAttribute.Name == "name" && elem.FirstAttribute.Value == name).First();
            return theElement;
            
        }


        private void ConstructGH2()
        {
            var root = doc.Root;
            var definition = findChunk(root, "Definition");
            var definitionObjects = findChunk(definition, "DefinitionObjects");
            Console.WriteLine(definitionObjects.Name.ToString());



        }

        private static void ClearChunks(GH_Chunk ParentChunk)
        {
            foreach (GH_Chunk chunk in ParentChunk.Chunks)
            {
                ParentChunk.RemoveChunk(chunk);
            }
            ParentChunk.RemoveItem("ObjectCount");
            ParentChunk.SetInt32("ObjectCount", 0, 0);
        }
        public static void AddChunk(GH_Chunk chunkToAddTo, GH_Chunk chunkToAdd)
        {
            MethodInfo setChunkMethodInfo = chunkToAddTo.GetType().GetMethod("AddChunk", BindingFlags.NonPublic | BindingFlags.Instance);

            setChunkMethodInfo.Invoke(chunkToAddTo, new object[] { chunkToAdd });
        }



        public void saveFile()
        {
            archive.WriteToFile(@"C:\users\aheumann\desktop\TestWriteFrom.ghx", true, false);
        }


    }
}
