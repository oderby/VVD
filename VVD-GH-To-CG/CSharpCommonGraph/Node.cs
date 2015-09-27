using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpCommonGraph
{
    public class Node
    {
        public string Type;
        public Guid InstanceGuid;
        public string Name;
        public List<Port> Ports;
        public MetaData Metadata;

    }

   
}
