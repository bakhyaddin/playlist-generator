arr = ["name", "TRHVKYA128F4289436,1,TRFONPG128F92FC00F,0.00404794,TRUCAXC128F92F9AF3,0.0029217,TRCTKVX128F425C70A,8.83503e-05,TRBUCVS128F423F5DD,0.000931335,TRZVOIJ128F931A735,0.00586252,TRTDSTI128F930122B,0.000178616,TRKZWHG128F930BF84,0.0178901,TRQXLCL128F930FB2B,0.00202357,TRQSBIL128F93032F3,0.00358385,TRVVDDN128F426BC56,0.00479434,TRHVKYA128F4289436,0.00100462,TRFONPG128F92FC00F,0.00404794,TRUCAXC128F92F9AF3,0.0029217,TRCTKVX128F425C70A,8.83503e-05,TRBUCVS128F423F5DD,0.000931335", "name1", "TRHVKYA128F4289436,0.00100462,TRFONPG128F92FC00F,0.00404794,TRUCAXC128F92F9AF3,0.0029217,TRCTKVX128F425C70A,8.83503e-05,TRBUCVS128F423F5DD,0.000931335,TRZVOIJ128F931A735,0.00586252"]
graphData = {1:{"similars": [2,4], "weights": [6,2]}, 2:{"similars": [1,4], "weights": [6,2]}}

nodes = set()

nodes.add(arr[0])
similars = arr[1].split(",")
for i in range(0, len(similars), 2):
    nodes.add(similars[i])

nodes = list(nodes)

N = len(nodes)

index = dict(zip(nodes,range(N)))

# for k in index:
#     print(k, index[k])




import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain

G = nx.Graph()

for node in graphData:
    for i in range(len(graphData[node]["similars"])):
        G.add_edge(node, graphData[node]["similars"][i], weight=graphData[node]["weights"][i])

# nx.draw(G, pos=nx.circular_layout(G), node_color='r', edge_color='b')
# plt.show()

partition = community_louvain.best_partition(G)

# for nid in partition:
    # ss = '%d,%d\n' % (nid,com)
    # print(ss)
    # print(nid, partition[nid])


# len(set(partition.values()))

# print(community_louvain.modularity(partition,G))

all_data = {}

for i in range(0, len(arr), 2):
    row_idx = arr[i]
    similars = arr[i+1].split(",")
    similarEdges = []
    weights = []
    for i in range(0,len(similars),2):
        if float(similars[i+1]) >= 0.5:
            similarEdges.append(similars[i])
            weights.append(similars[i+1])
    all_data.update({row_idx : {"similars" : similarEdges, "weights": weights}})
    print(len(similarEdges))
    print(len(weights))
    # similarEdges = []
    # weights = []

seed = str(input("Pick some songs to start your playlist: "))

seed_raw = seed.split(",")
print(seed_raw)
