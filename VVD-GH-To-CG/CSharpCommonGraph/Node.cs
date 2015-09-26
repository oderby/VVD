using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpCommonGraph
{
    public class Node
    {
        public String Type;
        public Guid InstanceGuid;
        public List<Port> Ports;
        public Metadata Metadata;

    }

    public class Metadata
    {
      public string Ignore;
      public string Inspect;
    }
}
