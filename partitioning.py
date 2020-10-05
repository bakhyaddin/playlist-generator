import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain

from preprocessing import Preprocessing

preprocessingClass = Preprocessing("lastfm_similars.db")
nodes = preprocessingClass.get_all_nodes()
indexes = preprocessingClass.giving_indexes_to_tIds(nodes)
allData = preprocessingClass.getting_all_data(indexes)

trackIds = []

inFile = open('track_list.txt')
for line in inFile:
    fields = line.strip().split('<S>')
    trackIds.append(fields[0])
inFile.close()

G = nx.Graph()

print("getting the graph start")
for node in allData:
    if(allData[node]["tid"] in trackIds):
        for i in range(len(allData[node]["similars"])):
            G.add_edge(node, allData[node]["similars"][i], weight=allData[node]["weights"][i])

# nx.draw(G, pos=nx.circular_layout(G), node_color='r', edge_color='b')
# plt.show()
print("getting the graph end")

# Compute the best partition
print("partitioning start")

partition = community_louvain.best_partition(G)

print("partitioning end")

# Store the partition dictionary to file
print("Store the partition dictionary to file start ")

outFile = open('partition.txt','w')
for nid in partition:
    community = partition[nid]
    ss = '%d,%d\n' % (nid, community)
    outFile.write(ss)
outFile.close()

print("Store the partition dictionary to file end")


# Number of communities
# 16172
print(len(set(partition.values())))

# Modularity of the partition
# 0.9377583051376279
print(community_louvain.modularity(partition,G))
