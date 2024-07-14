import networkx as nx
import numpy as np
import sys

k = int(sys.argv[1])

n = 1005 # Number of nodes

for i in range(1, k+1):
    network_file = "G_" + str(i) + ".edges"
    threshold_file = "Threshold_" + str(i) + ".edges"

    G = nx.read_edgelist(network_file)
    threshold_file_obj = open(threshold_file, 'w')

    for v in range(1, n+1): # all the nodes
        if G.has_node(str(v)):
            threshold = np.random.randint(1, G.degree[str(v)] + 2)

        else: # The node is an isolated node
            threshold = 1

        threshold_file_obj.write(str(v) + " " + str(threshold) + "\n")

    threshold_file_obj.close()
