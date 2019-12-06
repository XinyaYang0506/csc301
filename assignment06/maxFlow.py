from random import seed
from random import randint
import networkx as nx
import matplotlib.pyplot as plt

from networkx.drawing.nx_pydot import write_dot 

def flow_network_generator(i):
    filename = "input" + str(i) + ".dot"
    f= open(filename, "w+")
    f.write("digraph g{\n rankdir = LR\n")
    G = nx.MultiDiGraph(directed = True); 
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

def max_flow_generator(G, i):
    num_Nodes = G.number_of_nodes()
    s = randint(1, num_Nodes)
    while (G.out_degree(s) == 0): 
        s = randint(1, num_Nodes)

    t = s
    while True:
        if t != s and (G.out_degree(t) == 0 or randint(1, 2) == 1):
            break
        else:
            t = list(G[t])[0] #[0] is still general a random one in the list

    max_flow = 0

    while True:
        # an iteration
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
    
    filename = "output" + str(i) + ".dot"
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

def main():
  for i in range(10): 
      G = flow_network_generator(i+1)
      max_flow_generator(G, i+1)

if __name__ == "__main__":
    main()