using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using GH_IO;
using System.Xml.Serialization;
using System.IO;
using CSharpCommonGraph;

namespace VVD_GH_To_CG
{
    class Program
    {
        static void Main(string[] args)
        {
            string filePath = args[0];
            Console.WriteLine(filePath);
            CommonGraph dg = Parser.CommonGraphFromGHFile(filePath);
            XmlSerializer SerializerObj = new XmlSerializer(typeof(CommonGraph));
            TextWriter WriteFileStream = new StreamWriter(@"C:\Users\aheumann\Desktop\testOutput.cgx");
            SerializerObj.Serialize(WriteFileStream, dg);
 

            Console.ReadKey();

        }
    }
}
