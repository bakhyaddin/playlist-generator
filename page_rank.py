import os
import scipy.sparse
import sys
import sqlite3
import time
import numpy as np

from preprocessing import Preprocessing
from to_csv import TOCSV

preprocessingClass = Preprocessing("lastfm_similars.db")
nodes = preprocessingClass.get_all_nodes()
indexes = preprocessingClass.giving_indexes_to_tIds(nodes)
allData = preprocessingClass.getting_all_data(indexes)


# Read community partition dictionary
partition, comm = {}, {}
inFile = open('partition.txt')
for line in inFile:
    fields = line.strip().split(',')
    partition[int(fields[0])] = int(fields[1])
inFile.close()

for nid in partition:
    com = partition[nid]
    if com not in comm:
        comm[com] = []
    comm[com].append(nid)


# Read edge index and weight data (row,col,data) into list for coo_matrix generation
row,col,data=[],[],[]

for node in allData:
    for i in range(0, len(allData[node]["similars"])):
        row.append(node)
        col.append(allData[node]["similars"][i])
        data.append(allData[node]["weights"][i])


# getting csv file
toCsv = TOCSV(row, col, data)
toCsv.getCsvFile()

# Calculate the scipy csr format of the transition matrix

# number of nodes
N = len(indexes)

# calculate the graph adjacency matrix as a scipy sparse matrix
mtx = scipy.sparse.coo_matrix((data,(row,col)),shape=(N,N))
compress = "csr"
mtx = mtx.asformat(compress)


# normalize the matrix
rowSum = np.array(mtx.sum(axis=1)).flatten()
rowSum[rowSum != 0] = 1./rowSum[rowSum != 0]
invDiag = scipy.sparse.spdiags(rowSum.T, 0, N, N, format=compress)
mtx = invDiag * mtx


# identify sinking nodes index
sinking = np.where(rowSum == 0)[0]


# PageRank function
def PPR(indexes,mtx,sinking,v=None,alpha=0.85,max_iter=100, tol=1e-6):

    N = len(indexes)

    # starting rank
    x = np.repeat(1./N, N)

    # personalization vector
    if v is None:
        v = np.repeat(1./N, N)
    v /= v.sum()

    #power iteration:
    for _ in range(0, max_iter):
        xlast = x
        x = alpha*(x*mtx + sum(x[sinking])*v) + (1-alpha)*v
        if np.absolute(x-xlast).sum() < tol:
            #nodes = sorted(index, key=index.get, reverse=False)
            #return dict(zip(nodes,x))
            scores = {}
            for key in indexes:
                value = indexes[key]
                scores[key] = x[value]
            return scores
    raise RuntimeError('Power iteration failed to converge in %d iterations.' % max_iter)


# Map track id to song metadata

meta = {}
inFile = open('track_list.txt')
for line in inFile:
    fields = line.strip().split('<S>')
    meta[fields[0]] = fields[1] + ':' + fields[2]
inFile.close()


# Generate playlist from a subset of all the songs

seed = str(input("Pick some songs to start your playlist: "))

seed_raw = seed.split(";")

seed = []
for tid in meta:
    song = meta[tid].split(":")[1]
    for track in seed_raw:
        if song == track:
            seed.append(indexes[tid])


discover_rate = float(input("Pick discovery rate from 0 to 1: "))
listLength = int(input("Playlist length: "))

t0 = time.time()
v = np.repeat(discover_rate*0.01/float(N),N)
for track in seed:
    for song in comm[partition[track]]:
        v[song] = 1./N
for track in seed:
    v[track] = len(comm[partition[track]])/float(N)

rank = PPR(indexes, mtx, sinking, v)
playlist = sorted(rank, key=rank.get, reverse=True)
t1 = time.time()
scores = [rank[i] for i in playlist]
print("Playlist generated in %.3f seconds" % (t1-t0))
uniList = []
for i in range(0, listLength):
    song = meta[playlist[i]]
    if song not in uniList:
        uniList.append(song)

print(uniList)