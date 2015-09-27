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
                string dest = path.Replace(Path.GetExtension(path), ".dyn");
                if (args.Length > 1)
                {
                    dest = args[1];
                }

               

                CSharpCommonGraph.CommonGraph graphFromFile;
                // Construct an instance of the XmlSerializer with the type
                // of object that is being deserialized.
                XmlSerializer mySerializer =
                new XmlSerializer(typeof(CSharpCommonGraph.CommonGraph));
                // To read the file, create a FileStream.
                FileStream myFileStream =
                new FileStream(path, FileMode.Open);
                // Call the Deserialize method and cast to the object type.
                graphFromFile = (CSharpCommonGraph.CommonGraph)
                mySerializer.Deserialize(myFileStream);

                Console.WriteLine("now attempting to convert back to a new .dyn");

                var outdoc = new XmlDocument();
                CGToXML.SaveInternal(dest, graphFromFile);

            }


            catch (Exception e)
            {

                Console.WriteLine(e.Message);
                Console.WriteLine(e.StackTrace);
            }
        }

    }
}
