#we need to split a group of people into two teams. 
#we know that people want to be on a team with their friends
#how do we pick teams of the same size? 
#relationships are given in a graph format - you want to set up the reds and blues so there are as few red-to-blue connections as possible

import networkx as nx
from collections import defaultdict
from dwave.system import DWaveSampler, EmbeddingComposite

G = nx.Graph()
G.add_edges_from([(0,4), (0,5), (1,2), (1,6), (2,4), (3,7), (5,6), (6,7) ])

Q = defaultdict(int)

#Constraint - only two teams
lagrange = 4

for i in range(8): 
    Q[(i,i)] += -7 * lagrange
    for j in range(i+1, 8): 
        Q[(i, j)] += 2*lagrange

#Objective - minimize the number of friends split up (e.g. have an edge between them)
for i,j in G.edges: 
    Q[(i,i)] += 1
    Q[(j,j)] += 1
    Q[(i,j)] += -2

sampler = EmbeddingComposite(DWaveSampler())

sampleset = sampler.sample_qubo(Q, num_reads=10)

print(sampleset)
