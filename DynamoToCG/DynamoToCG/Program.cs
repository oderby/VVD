using System;
using System.IO;
using System.Linq;
using System.Xml;
using System.Xml.Serialization;


namespace DynamoToCG
{
    internal class Program
    {
        [STAThread]
        static internal void Main(string[] args)
        {

            try
            {
             var path = args[0];
                string dest = path.Replace(Path.GetExtension(path), ".cgx");
            if (args.Length>1){
               dest = args[1];
               
            }

               var doc = new XmlDocument();
                doc.Load(path);

                var graph = NodeGraph.LoadGraphFromXml(doc);
                foreach (var node in graph.Nodes)
                {
                    Console.WriteLine(node.Type);
                    foreach(var port in node.Ports){
                        Console.WriteLine(port.InstanceGuid);
                    }
                }

                foreach (var connector in graph.Connectors)
                {
                    Console.WriteLine("edge from "+(graph.Nodes.Where(x=>x.Ports.Select(port=>port.InstanceGuid).ToList().Contains(connector.SrcGuid)).First().Type));
                    Console.WriteLine(" to"+(graph.Nodes.Where(x=>x.Ports.Select(port=>port.InstanceGuid).ToList().Contains(connector.DestGuid)).First().Type));
                }

                System.Xml.Serialization.XmlSerializer xser = new System.Xml.Serialization.XmlSerializer(typeof(CSharpCommonGraph.CommonGraph));
                TextWriter WriteFileStream = new StreamWriter(dest);
                xser.Serialize(WriteFileStream, NodeGraph.ToCommonCgraph(graph));
                Console.WriteLine("saved CG to disk");
                WriteFileStream.Close();

                
               
            }
               
              
            catch (Exception e)
            {
              
                Console.WriteLine(e.Message);
                Console.WriteLine(e.StackTrace);
            }
        }

    }
}
