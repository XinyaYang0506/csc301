from random import seed
from random import randint
import networkx as nx
import os
from networkx.drawing.nx_pydot import write_dot


class flow:
    # This function randomly generated a directed graph with weighted edge as its capacity
    # i is the number for dot file
    @staticmethod
    def flow_network_generator(i):
        filename = "input/input" + str(i)
        dot_filename = filename + ".dot"
        f = open(dot_filename, "w+")
        f.write("digraph g{\n rankdir = LR\n")
        G = nx.MultiDiGraph(directed=True)

        num_Nodes = randint(5, 15)  # specified in the assignment prompt
        for node in range(num_Nodes):
            G.add_node(node + 1)
            # one-base
            f.write("%d;\n" % (node + 1))

        num_Edges = randint(num_Nodes - 1, num_Nodes * (num_Nodes - 1) / 2)

        # generate some edge
        for _ in range(num_Edges):
            from_Node = 0
            to_Node = 0
            while from_Node == 0 or G.has_edge(
                from_Node, to_Node
            ):  # avoid parallel edge/reversed parallel edge
                from_Node = randint(1, num_Nodes)
                to_Node = from_Node
                while to_Node == from_Node:  # to_Node should not == from_Node
                    to_Node = randint(1, num_Nodes)

            edge_weight = randint(1, 100)  # magic number

            G.add_edge(from_Node, to_Node, capacity=edge_weight, flow=0)
            G.add_edge(to_Node, from_Node, capacity=0, flow=0)  # residual
            f.write('%d -> %d [label = " %d "];\n' % (from_Node, to_Node, edge_weight))

        f.write('label = "graph %d"\n' % (i))
        f.write("}\n")
        f.close()
        command = "dot -Tpng " + filename + ".dot -o " + filename + ".png"
        os.system(command)
        return G

    # This function will select s, the source node and t, the sink node almost randomly.
    # There will be at least a path from s to t so the max flow between s and t will always > 0
    @staticmethod
    def select_nodes(G):
        num_Nodes = G.number_of_nodes()
        s = randint(1, num_Nodes)
        counter = 0  # real out degree, residual edges excluded
        for to_Node in list(G[s]):
            capacity = G[s][to_Node][0]["capacity"]
            if capacity > 0:
                counter += 1
        while counter == 0:
            s = randint(1, num_Nodes)
            for to_Node in list(G[s]):
                capacity = G[s][to_Node][0]["capacity"]
                if capacity > 0:
                    counter += 1

        t = s
        while True:
            if t != s and randint(1, 2) == 1:  # add some randomness
                break
            else:
                found = False
                for to_Node in list(G[t]):
                    capacity = G[t][to_Node][0]["capacity"]
                    if capacity > 0:  # next node needed to be connected by real edge
                        t = to_Node
                        found = True
                        break
                if not found:
                    break
        return (s, t)
