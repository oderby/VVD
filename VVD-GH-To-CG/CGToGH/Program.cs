using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Serialization;

namespace CGToGH
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("hello!");
           
            try
            {
                var path = args[0];
                string dest = path.Replace(Path.GetExtension(path), "_Generated.ghx");
                if (args.Length > 1)
                {
                    dest = args[1];
                }

                CSharpCommonGraph.CommonGraph graphFromFile = DeserializeCG(path);

                Console.WriteLine("now attempting to convert back to a new .gh");

                GH_FileComposer composer = new GH_FileComposer(graphFromFile);
                composer.SaveFile(dest);
               // Console.ReadKey();

            }


            catch (Exception e)
            {

                Console.WriteLine(e.Message);
                Console.WriteLine(e.StackTrace);
            }

        }

        private static CSharpCommonGraph.CommonGraph DeserializeCG(string path)
        {
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
            return graphFromFile;
        }
    }
}
