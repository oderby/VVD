using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Serialization;

namespace CSharpCommonGraph
{
   public class Port
    {
       [XmlAttribute("InstanceGuid")]
       public string InstanceGuid;
       [XmlAttribute("Name")]
       public string Name;
       public MetaData MetaData = new MetaData();
       

    }
}
