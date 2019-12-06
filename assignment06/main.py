from flow import flow
from max_flow import max_flow

def main():
  for i in range(1): 
      G = flow.flow_network_generator(i+20)
      (s, t) = flow.select_nodes(G)
      max_flow.max_flow_generator(G, i+20, s, t)

if __name__ == "__main__":
    main()