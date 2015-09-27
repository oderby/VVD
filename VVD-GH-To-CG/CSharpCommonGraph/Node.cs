using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Serialization;

namespace CSharpCommonGraph
{
    public class Node
    {
        [XmlAttribute("Type")]
        public string Type;
        [XmlAttribute("InstanceGuid")]
        public string InstanceGuid;
        [XmlAttribute("Name")]
        public string Name;
        public List<Port> Ports = new List<Port>();
        public MetaData MetaData = new MetaData();
        public Position Position = new Position();

    }

    public class Position
    {
        public double X;
        public double Y;
    }

   
}
