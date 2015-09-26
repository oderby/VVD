using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpCommonGraph
{
    [Serializable()]
    public class CommonGraph
    {
      public List<Edge> Edges;
      public List<Node> Nodes;
      public List<Port> Ports;

      //empty constructor for the purposes of XMLSerializer
      public CommonGraph()
      {
         
          Edges = new List<Edge>();
          Nodes = new List<Node>();
          Ports = new List<Port>();
      }


      }

      
    
}
