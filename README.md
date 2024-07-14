# Learning-Multilayer-Dynamical-Systems-ICML24

Paper: *Efficient PAC Learnability of Dynamical Systems Over Multilayer Networks*
<br/>
**Full version** (contains complete proofs of theorems): [https://arxiv.org/pdf/2405.06884]

## Directory structure:

1. **analysis/**: the code for learning

2. **networks/**: selected networks
- Real networks: Aarhus, CKM-Phy, PPI, Twitter
- Synthetic networks:  Gnp

## To run the code

1. `cd analysis`
2. `python3 learn.py [network_type] [network_name] [training_set_size]`
- network_type: real, synthetic
- network_name: Aarhus, CKM-Phy, PPI, Twitter, Gnp
- training_set_size: integer >= 1

### Example 1: Learning for Aarhus network with 1000 training examples:
`python3 learn.py real Aarhus 1000`


### Example 2: Learning for Gnp network with 1000 training examples:
`python3 learn.py synthetic Gnp 1000`
