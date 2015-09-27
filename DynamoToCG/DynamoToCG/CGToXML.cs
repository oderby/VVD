using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace DynamoToCG
{
    public static class CGToXML
    {
        public static bool PopulateXmlDocument(XmlDocument xmlDoc, CSharpCommonGraph.CommonGraph cg)
        {
            try
            {
                //TODO read this stuff from the metadata from the cg
                var root = xmlDoc.DocumentElement;
                root.SetAttribute("Version", (.83).ToString());
                root.SetAttribute("X", 0.ToString(CultureInfo.InvariantCulture));
                root.SetAttribute("Y", 0.ToString(CultureInfo.InvariantCulture));
                root.SetAttribute("zoom", 1.0.ToString(CultureInfo.InvariantCulture));
                root.SetAttribute("Name", "a diff file");
                root.SetAttribute("Description", "a diff");

            

                var elementList = xmlDoc.CreateElement("Elements");
                //write the root element
                root.AppendChild(elementList);
                              
                foreach (var dynEl in cg.Nodes.Select(el =>  el.Metadata.Inspect)){
                    var doc = new XmlDocument();
                    doc.LoadXml(dynEl);

                    //necessary for crossing XmlDocument contexts
                    XmlNode importNode = elementList.OwnerDocument.ImportNode(doc.DocumentElement, true);

                   elementList.AppendChild(importNode);
                }
                

                //write only the output connectors
                var connectorList = xmlDoc.CreateElement("Connectors");
                //write the root element
                root.AppendChild(connectorList);

                foreach (var el in cg.Nodes)
                {
                    foreach (var port in el.Ports.Where(x=>x.MetaData.Inspect.Contains("end")).ToList())
                    {
                        foreach (
                            var c in
                                cg.Edges.Where(edge=>edge.SrcGuid.Contains(edge.SrcGuid)).ToList())
                        {
                            var connector = xmlDoc.CreateElement("Dynamo.Models.ConnectorModel");
                            connectorList.AppendChild(connector);
                            connector.SetAttribute("start", c.SrcGuid.Split('_').First());
                            connector.SetAttribute("start_index", c.SrcGuid.Split('_').ToList()[1].Replace("OUT",""));
                            connector.SetAttribute("end", c.DestGuid.Split('_').First());
                            connector.SetAttribute("end_index", c.DestGuid.Split('_').ToList()[1].Replace("IN",""));

                            if (c.DestGuid.Split('_').ToList()[1] == "start")
                                connector.SetAttribute("portType", "0");
                        }
                    }
                }

                //save the annotation
               /* var annotationList = xmlDoc.CreateElement("Annotations");
                root.AppendChild(annotationList);
                foreach (var n in annotations)
                {
                    var annotation = n.Serialize(xmlDoc, SaveContext.File);
                    annotationList.AppendChild(annotation);
                }

             */ 
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                Console.WriteLine(ex.StackTrace);
                return false;
            }
        }

        public static bool SaveInternal(string targetFilePath,CSharpCommonGraph.CommonGraph cg)
        {
            // Create the xml document to write to.
            var document = new XmlDocument();
            document.CreateXmlDeclaration("1.0", null, null);
            document.AppendChild(document.CreateElement("Workspace"));

           // Utils.SetDocumentXmlPath(document, targetFilePath);

            if (!PopulateXmlDocument(document,cg))
                return false;

            try
            {
               
                document.Save(targetFilePath);
            }
            catch (IOException)
            {
                return false;
            }

          
            return true;
        }

    }
}
