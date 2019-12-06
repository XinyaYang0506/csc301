from random import seed
from random import randint
import networkx as nx
import os

from networkx.drawing.nx_pydot import write_dot


class max_flow:

    # this function will calculate the max flow of G, a directed, edge-weighted graph.
    # s is the source node, t is the sink node.
    # side-effect: generate a dot file numbered as i representing the flow.
    @staticmethod
    def max_flow_generator(G, i, s, t):
        max_flow = 0
        num_Nodes = G.number_of_nodes()

        while True:
            queue = [s]  # the nodes waiting to be explored
            pred = [-1] * (num_Nodes + 1)  # value - index is a edge

            while queue != []:  # the end of BFS
                cur_Node = queue.pop(0)
                for to_Node in list(G[cur_Node]):  # all the out edge adjs
                    if (
                        pred[to_Node] == -1  # haven't been explored
                        and to_Node != s  # not the start node
                        and G[cur_Node][to_Node][0]["capacity"]
                        > G[cur_Node][to_Node][0]["flow"]  # not saturated
                    ):
                        pred[to_Node] = cur_Node
                        queue.append(to_Node)

            if pred[t] != -1:  # there is an augmented path
                add_flow = G[pred[t]][t][0]["capacity"] - G[pred[t]][t][0]["flow"]
                node = t
                while node != s:  # find the add_flow, which is min of capacity - flow
                    add_flow = min(
                        add_flow,
                        G[pred[node]][node][0]["capacity"]
                        - G[pred[node]][node][0]["flow"],
                    )
                    node = pred[node]

                node = t
                while node != s:  # update the edge
                    G[pred[node]][node][0]["flow"] += add_flow
                    G[node][pred[node]][0]["flow"] -= add_flow  # residual
                    node = pred[node]

                max_flow += add_flow
            else:
                break  # found the maxflow

        filename = "output/output" + str(i)
        dot_filename = filename + ".dot"
        f = open(dot_filename, "w+")
        f.write("digraph g{\n rankdir = LR\n")
        for edge in list(G.edges):
            capacity = G[edge[0]][edge[1]][0]["capacity"]
            if capacity != 0:
                flow = G[edge[0]][edge[1]][0]["flow"]
                if flow != 0:
                    f.write(
                        '%d -> %d [label = " %d/%d "];\n'
                        % (edge[0], edge[1], flow, capacity)
                    )
        f.write(
            'label = "graph %2d: maximum flow = %d, s = %d, t = %d"\n'
            % (i, max_flow, s, t)
        )
        f.write("}\n")
        f.close()
        command = "dot -Tpng " + filename + ".dot -o " + filename + ".png"
        os.system(command)

