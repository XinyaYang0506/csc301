from random import seed
from random import randint
import networkx as nx

from networkx.drawing.nx_pydot import write_dot 
class max_flow:
    @staticmethod
    def max_flow_generator(G, i, s, t):
        max_flow = 0
        num_Nodes = G.number_of_nodes()
        
        while True:
            queue = [s] 
            pred = [-1]*(num_Nodes + 1) #value - index is a edge

            while queue != []: #the end of BFS
                cur_Node = queue.pop(0)
                for to_Node in list(G[cur_Node]): #all the out edge adjs
                    if pred[to_Node] == -1 and to_Node != s and G[cur_Node][to_Node][0]['capacity'] > G[cur_Node][to_Node][0]['flow']:
                        pred[to_Node] = cur_Node
                        queue.append(to_Node)
                
            if pred[t] != -1: #there is an augmented path
                add_flow = G[pred[t]][t][0]['capacity'] - G[pred[t]][t][0]['flow']
                node = t
                while (node != s): #find the flow
                    add_flow = min(add_flow, G[pred[node]][node][0]['capacity'] - G[pred[node]][node][0]['flow'])
                    node = pred[node]

                node = t
                while (node != s): #update the flow
                    G[pred[node]][node][0]['flow'] += add_flow
                    G[node][pred[node]][0]['flow'] -= add_flow
                    node = pred[node]
                
                max_flow += add_flow
            else: 
                break
        
        filename = "output_graphs/output" + str(i) + ".dot"
        f= open(filename, "w+")
        f.write("digraph g{\n rankdir = LR\n")
        for edge in list(G.edges): 
            capacity = G[edge[0]][edge[1]][0]['capacity']
            if capacity != 0:
                flow = G[edge[0]][edge[1]][0]['flow']
                if flow != 0:
                    f.write("%d -> %d [label = \" %d/%d \"];\n" % (edge[0] , edge[1] , flow, capacity))
        f.write("label = \"graph %2d: maximum flow = %d, s = %d, t = %d\"\n" % (i, max_flow, s, t))
        f.write("}\n")
        f.close()

