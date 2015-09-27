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



namespace CGToGH
{
    public class GH_FileComposer
    {
        CommonGraph graph;
        XDocument doc;
        public GH_FileComposer(CommonGraph cg)
        {
            graph = cg;

            doc = XDocument.Parse(graph.MetaData.Ignore);

            //File.WriteAllText(@"C:\Users\aheumann\Desktop\xml out test.txt", graph.MetaData.Ignore);
           

            ConstructGH();
        }

 

        XElement findChunk(XElement node, string name)
        {
            var Chunks = node.Elements().Where(elem => elem.Name == "chunks").First();
            var theElement = Chunks.Elements().Where(elem => elem.FirstAttribute.Name == "name" && elem.FirstAttribute.Value == name).First();
            return theElement;
            
        }

        IEnumerable<XElement> getChunks(XElement node)
        {
            var Chunks = node.Elements().Where(elem => elem.Name == "chunks").First();
            return Chunks.Elements();
        }

        string elementName(XElement elem)
        {
            return elem.FirstAttribute.Value;
        }


        private void ConstructGH()
        {
            var root = doc.Root;
            var definition = findChunk(root, "Definition");
            var definitionObjects = findChunk(definition, "DefinitionObjects");
            var objChunks = getChunks(definitionObjects);
           



            List<XElement> nodesFromGraph = new List<XElement>();
           
            foreach (Node n in graph.Nodes)
            {
                nodesFromGraph.Add(ElementFromNode(n));

            }

   
            int i=0;
            foreach (XElement nodeFromGraph in nodesFromGraph)
            {
                try
                {
                  //  Console.WriteLine(elementName(nodeFromGraph));
                 //   nodeFromGraph.SetAttributeValue(XName.Get("index"), i);
                    i++;
                }
                catch { }
               
            }

            var items = definitionObjects.Elements().Where(elem => elem.Name == "items").First();

            
            var objectCount = items.Elements().Where(elem => elementName(elem) == "ObjectCount").First();

            int newCount = nodesFromGraph.Count;
            objectCount.Value = newCount.ToString();

            objChunks.First().Parent.ReplaceAll(nodesFromGraph.ToArray());
          //  foreach (XElement objChunk in objChunks)
          //  {
           //     objChunk.Parent.ReplaceAll(dummyElement);
              //  objChunk.Remove();
         //   }


            

        }

        public void SaveFile(string savePath)
        {


            doc.Save(savePath);
        }

        private static XElement ElementFromNode(Node n)
        {
            XElement testElem = null;
            string objectXML = n.MetaData.Ignore;
            Console.WriteLine(objectXML);
            try
            {
                testElem = XElement.Parse(objectXML);
                Console.WriteLine("foo foo"+testElem.Name);
            }
            catch (Exception e)
            {
             
            }
            return testElem;
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



       


    }
}
