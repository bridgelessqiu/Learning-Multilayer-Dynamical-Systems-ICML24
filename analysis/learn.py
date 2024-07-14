import numpy as np
import networkx as nx
import random
import sys

# Preliminary
size_map = {"Aarhus" : 61, "Gnp" : 500}
layer_map = {"Aarhus" : 5, "Gnp" : 2}

# Inputs
network_type = sys.argv[1] # real, synthetic
network_name = sys.argv[2] # Aarhus, Gnp
train_s = int(sys.argv[3]) # Size of the training set

# Varialbes
n = size_map[network_name] # number of vertices
k = layer_map[network_name] # number of layers

sigma = n # Learn the thresholds of all the vertices
test_s = 100 # size of the test set to compute the loss

prob = 0.5 # Uniform distribution


# ---------- Constructing Target Network ---------- #

# Multilayer networks
# M[0] is discarded to make index match
M = [None] * (k + 1) # layers: M[i] is the graph on the ith layer

# TH[0] is discarded to make index match
TH = [None] * (k + 1) # TH[i] is the vector that consists of the thresholds on G_i

# Read in the networks and the thresholds
for i in range(1, k+1):
    network_file = "../networks/" + network_type + "/" + network_name + "/G_" + str(i) + ".edges"
    threshold_file = "../networks/" + network_type + "/" + network_name +"/Threshold_" + str(i) + ".edges"

    G = nx.read_edgelist(network_file)
    M[i] = G
    
    threshold_vec = {}
    with open(threshold_file, 'r') as file:
        for line in file:
            ver = str(line.split(' ')[0])
            thr = int(line.split(' ')[1])
            threshold_vec[ver] = thr

    TH[i] = dict(threshold_vec)


print("----------- Training starts -------------- \n")

# --------- Learning ----------- #

# Python deep copy
TH_learned = [dict(x) for x in TH[1:]]
TH_learned.insert(0, None)

# The set of vertices whose thresholds are unknown
lst = list(range(1, n + 1))
random.shuffle(lst)
V_prime = lst[:sigma]

to_learn = [0] * (n + 1)
for u in V_prime:
    to_learn[u] = 1

# Replace the threhsolds of vertices in V_prime to 0 (and will learn them) in TH_learned
for u in V_prime:
    for l in range(1, k+1):
        TH_learned[l][str(u)] = 0

for _ in range(train_s):
    # C sampled from D
    # C[0] is discarded, to make the indice match better
    C = np.random.choice([0, 1], size=(n + 1,), p=[prob, float(1 - prob)]) # Uniform distribution

    # h^*(C) is computed
    for u in range(1, n + 1):
        OR_flag = False # The threshold condition
        score = [0] * (k + 1) # Scores of u in each layer

        for l in range(1, k + 1): # Layers
            score[l] = C[int(u)] # Score of u in G_l under C, counting own state

            if M[l].has_node(str(u)): # that means u is not isolated in the lth layer
                for v in M[l][str(u)]:
                    score[l] += C[int(v)] 
        
            if score[l] >= TH[l][str(u)]: # If the threshold  condition is satisfied
                OR_flag = True
                break

        if not OR_flag and to_learn[int(u)] == 1:
            for l in range(1, k + 1):
                TH_learned[l][str(u)] = max(TH_learned[l][str(u)], score[l] + 1)

# --------- Testing ----------- #
total_correct = 0

for _ in range(test_s):
    # C sampled from D
    # C[0] is discarded, to make the indice match better
    C = np.random.choice([0, 1], size=(n + 1,), p=[prob, float(1 - prob)]) # distribution

    learned_wrong_flag = False

    # h(C) and h^*(C) are computed
    for u in range(1, n + 1):
        OR_flag_true = False # The threshold condition for h^*
        OR_flag_learned = False # The threshold condition for h

        score = [0] * (k + 1) # Scores of u in each layer

        for l in range(1, k + 1): # Layers
            score[l] = C[int(u)] # Score of u in G_l under C, counting own state

            if M[l].has_node(str(u)): # that means u is not isolated in the lth layer
                for v in M[l][str(u)]:
                    score[l] += C[int(v)] 
        
            if score[l] >= TH[l][str(u)]: # If the threshold  condition is satisfied for h^*
                OR_flag_true = True

            if score[l] >= TH_learned[l][str(u)]: # If the threshold  condition is satisfied for h
                OR_flag_learned = True
    
        if OR_flag_true != OR_flag_learned:
            learned_wrong_flag = True
            break

    if not learned_wrong_flag:
        total_correct += 1

er = 1 - float(total_correct / test_s)

print("Error rate: {}\n".format(float(er)))
