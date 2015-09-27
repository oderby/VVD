using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Serialization;

namespace CSharpCommonGraph
{
    public class Edge
    {
        [XmlAttribute("SrcGuid")]
      public string SrcGuid;
        [XmlAttribute("DstGuid")]
      public string DestGuid;
        [XmlAttribute("InstanceGuid")]
      public string InstanceGuid;
    }
}
