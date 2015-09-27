using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using GH_IO;
using System.Xml.Serialization;
using System.IO;
using CSharpCommonGraph;
using IronPython.Runtime;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting.Providers;

namespace VVD_GH_To_CG
{
    class Program
    {
        static void Main(string[] args)
        {
            string filePath = args[0];
            //Console.WriteLine(filePath);
            CommonGraph dg = Parser.CommonGraphFromGHFile(filePath);
            XmlSerializer SerializerObj = new XmlSerializer(typeof(CommonGraph));
            string dest = filePath.Replace(Path.GetExtension(filePath), ".cgx");
            //Console.WriteLine(args.Length.ToString());
            if (args.Length>1){
               dest = args[1];
            }
            TextWriter WriteFileStream = new StreamWriter(dest);
            SerializerObj.Serialize(WriteFileStream, dg);

           
         //Console.ReadKey();

        }

        private static void DoThePython()
        {

            var engine = Python.CreateEngine();

            PythonContext context = HostingHelpers.GetLanguageContext(engine) as PythonContext;
            ICollection<string> paths = context.GetSearchPaths();
            paths.Add(@"C:\Program Files (x86)\IronPython 2.7\Lib");
            context.SetSearchPaths(paths);
            engine.ImportModule("xml");
            engine.Runtime.LoadAssembly(System.Reflection.Assembly.GetEntryAssembly());
            var scope = engine.CreateScope();
            engine.ExecuteFile(@"C:\Users\aheumann\Documents\vvd\CommonGraphDiffer.py", scope);
            var xmlToDS = scope.GetVariable<Func<string, dynamic>>("XMLToDS");
            var myDS = xmlToDS(@"C:\Users\aheumann\Documents\vvd\foo.dsx");
            foreach (var change in myDS.Changes)
            {
                
                //Console.WriteLine(change.ToString());


            }

        }
    }
}
