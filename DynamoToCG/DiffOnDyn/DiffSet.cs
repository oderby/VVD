using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Serialization;
using CSharpCommonGraph;

namespace DiffOnDyn
{
    [Serializable]
    public class DiffSet{
        public List<Change> Changes;
    

       public DiffSet()
       {
            Changes = new List<Change>();
       }
           

    }


    public class Change
    {
        [XmlAttribute("Status")]
        public string Status;
        [XmlAttribute("InstanceGuid")]
        public string InstanceGuid;
        public MetaData MetaData = new MetaData();
        public Change()
        {
            Status = string.Empty;
            InstanceGuid = string.Empty;
            
        }

    }

    public class NodeChange : Change
    {
         [XmlAttribute("Type")]
         public String Type;
         public Position Position = new Position();
        
        
        public NodeChange():base()
        {
            Type = string.Empty;
            
        }

    }

   public class PortChange : Change
    {
        [XmlAttribute("ParentGuid")]
        public String ParentGuid;
       

        public PortChange()
            : base()
        {
           
        }

    }

   public class EdgeChange : Change
    {
        [XmlAttribute("SrcGuid")]
        public String SrcGuid;
        [XmlAttribute("DstGuid")]
        public String DstGuid;

        public EdgeChange()
            : base()
        {

        }

    }

}
