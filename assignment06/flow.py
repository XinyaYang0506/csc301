from random import seed
from random import randint
import networkx as nx

from networkx.drawing.nx_pydot import write_dot 
class flow:
    @staticmethod
    def flow_network_generator(i):
        filename = "input_graphs/input" + str(i) + ".dot"
        f= open(filename, "w+")
        f.write("digraph g{\n rankdir = LR\n")
        G = nx.MultiDiGraph(directed = True)
        num_Nodes = randint(5, 15); #magic number 

        for node in range(num_Nodes):
            G.add_node(node + 1); #one-base
            f.write("%d;\n" % (node + 1))

        num_Edges = randint(num_Nodes - 1, num_Nodes * (num_Nodes - 1)/2); 

        # generate some edge
        for _ in range(num_Edges):
            from_Node = 0
            to_Node = 0
            while (from_Node == 0 or G.has_edge(from_Node, to_Node)):
                from_Node = randint(1, num_Nodes); 
                to_Node = from_Node; 
                while to_Node == from_Node:
                    to_Node = randint(1, num_Nodes); 

            edge_weight = randint(1, 100); #magic number

            G.add_edge(from_Node, to_Node, capacity = edge_weight, flow = 0)
            G.add_edge(to_Node, from_Node, capacity = 0, flow = 0)
            f.write("%d -> %d [label = \" %d \"];\n" % (from_Node , to_Node , edge_weight))
        
        f.write("label = \"graph %d\"\n" % (i))
        f.write("}\n")
        f.close()

        return G