#%%
from random import seed
from random import randint
import networkx as nx
import matplotlib.pyplot as plt

def flow_network_generator():
    #%%
    G = nx.DiGraph(); 

    num_Nodes = randint(1, 10); #magic number 
    #%%
    for node in range(num_Nodes):
        G.add_node(node + 1); #one-base

    #%% 
    num_Edges = randint(1, num_Nodes * (num_Nodes - 1)/2); 

    # generate some edge
    for _ in range(num_Edges):
        from_Node = randint(1, num_Nodes); 
        to_Node = from_Node; 
        while to_Node == from_Node:
            to_Node = randint(1, num_Nodes); 
        edge_weight = randint(1, 100); #magic number
        G.add_weighted_edges_from([(from_Node, to_Node, edge_weight)])

    #%%
    # plt.subplot(121)
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()

    return G
def max_flow_generator():


# %%
