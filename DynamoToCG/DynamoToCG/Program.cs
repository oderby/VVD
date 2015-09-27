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
                Console.WriteLine(args);
                var path = args[0];

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

                Console.ReadLine();

                System.Xml.Serialization.XmlSerializer xser = new System.Xml.Serialization.XmlSerializer(typeof(CSharpCommonGraph.CommonGraph));
                TextWriter WriteFileStream = new StreamWriter(@"C:\Users\Mike\Desktop\testOutput.cgx");
                xser.Serialize(WriteFileStream, NodeGraph.ToCommonCgraph(graph));
                Console.WriteLine("saved CG to disk");
                Console.ReadLine();
                WriteFileStream.Close();

                CSharpCommonGraph.CommonGraph graphFromFile;
                // Construct an instance of the XmlSerializer with the type
                // of object that is being deserialized.
                XmlSerializer mySerializer = 
                new XmlSerializer(typeof( CSharpCommonGraph.CommonGraph));
                // To read the file, create a FileStream.
                FileStream myFileStream = 
                new FileStream("C:\\Users\\Mike\\Desktop\\testOutput.cgx", FileMode.Open);
                // Call the Deserialize method and cast to the object type.
                graphFromFile = (CSharpCommonGraph.CommonGraph)
                mySerializer.Deserialize(myFileStream);

                Console.WriteLine("now attempting to convert back to a new .dyn");

                var outdoc = new XmlDocument();
                CGToXML.SaveInternal("C:\\Users\\Mike\\Desktop\\testOutput.dyn",graphFromFile);
               
               

            }
               
              
            catch (Exception e)
            {
              
                Console.WriteLine(e.Message);
                Console.WriteLine(e.StackTrace);
            }
        }

    }
}
