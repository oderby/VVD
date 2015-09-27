using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Serialization;

namespace DiffOnDyn
{
    class Program
    {
          static void Main(string[] args)
          {
              //take in a dynamo file and a diffset file
              //iterate the diffs and then make annotations in the dyn
              //depending on the kind of diff we do something different...use different colors
              //for instance
              try
              {
               var dynpath = args[0];
                var diffpath = args[1];

                var doc = new XmlDocument();
                doc.Load(dynpath);
                Console.WriteLine("now attempting to deserialze the diff file ");

                  //deserialze the diffset
                DiffOnDyn.DiffSet diffFromFile;
                // Construct an instance of the XmlSerializer with the type
                // of object that is being deserialized.
                XmlSerializer mySerializer =
                new XmlSerializer(typeof(DiffOnDyn.DiffSet));
                // To read the file, create a FileStream.
                FileStream myFileStream =
                new FileStream(diffpath, FileMode.Open);
                // Call the Deserialize method and cast to the object type.
                diffFromFile = (DiffOnDyn.DiffSet)
                mySerializer.Deserialize(myFileStream);

                Console.WriteLine("now attempting to generate annotations ");

                foreach (var change in diffFromFile.Changes)
                {
                    if (change is NodeChange)
                    {
                        if (change.Status == "added")
                        {
                            //add a new node and color it green...
                        }

                        if (change.Status == "removed")
                        {
                           //color an existing node red by adding to red group 
                        }
                    }
                }

                var outdoc = new XmlDocument();
               // CGToXML.SaveInternal(dest, diffFromFile);


                  //now apply the diff, this will create some groups for now
              }

                    catch (Exception e)
              {
              
                  Console.WriteLine(e.Message);
                  Console.WriteLine(e.StackTrace);
              }
          }

     


             /*  public static bool SaveInternal(string targetFilePath,CSharpCommonGraph.CommonGraph cg)
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
        */
         
    }
}