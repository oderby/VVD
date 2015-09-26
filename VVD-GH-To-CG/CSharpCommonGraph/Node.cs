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
        List<Port> Ports;
        Metadata Metadata;

    }

    public class Metadata
    {
        string Ignore;
        string Inspect;
    }
}
