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
    @staticmethod
    def select_nodes(G):
        num_Nodes = G.number_of_nodes()
        s = randint(1, num_Nodes)
        counter = 0
        for to_Node in list(G[s]):
            capacity = G[s][to_Node][0]['capacity']
            if capacity > 0: 
                counter += 1
        while (counter == 0): 
            s = randint(1, num_Nodes)
            for to_Node in list(G[s]):
                capacity = G[s][to_Node][0]['capacity']
                if capacity > 0: 
                    counter += 1

        t = s
        while True:
            if t != s and randint(1, 2) == 1:
                break
            else:
                found = False
                for to_Node in list(G[t]): #[0] is still general a random one in the list
                    capacity = G[t][to_Node][0]['capacity']
                    if (capacity > 0): 
                        t = to_Node
                        found = True
                        break
                if not found:
                    break
        return (s, t)