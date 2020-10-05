# swe-592_final-project
import os
import sys
import sqlite3

class Preprocessing:
    lastfm_database = None

    def __init__(self, lastfm_database):
        self.lastfm_database = lastfm_database

    def get_all_nodes(self):
        print("getting all nodes start")
        nodes = set()
        conn = sqlite3.connect(self.lastfm_database)
        cur = conn.cursor()
        cur.execute("SELECT tid, target FROM similars_src")
        while True:
            song = cur.fetchone()
            if not song:
                break
            nodes.add(song[0])
            similars = song[1].split(",")
            # weights = song[1].split(",")[1]
            for i in range(0, len(similars), 2):
                nodes.add(similars[i])
        conn.close()

        nodes = list(nodes)

        print("getting all nodes end")

        return nodes


    # definening indexes for each song in a new DB

    def giving_indexes_to_tIds(self, nodes):

        print("giving_indexes_to_tIds start")
        N = len(nodes)
        indexes = dict(zip(nodes, range(N)))

        print("giving_indexes_to_tIds end")

        return indexes


    def getting_all_data(self, indexes):
        print("getting all data start")
        all_data = {}

        conn = sqlite3.connect(self.lastfm_database)
        cur = conn.cursor()
        cur.execute("SELECT tid, target FROM similars_src")
        while True:
            song = cur.fetchone()
            if not song:
                break
            similars = song[1].split(",")
            row_idx = indexes[song[0]]

            similarEdges = []
            weights = []
            for i in range(0,len(similars),2):
                if float(similars[i+1]) >= 0.5:
                    similarEdges.append(indexes[similars[i]])
                    weights.append(float(similars[i+1]))
            all_data.update({row_idx : {"similars" : similarEdges, "weights": weights, "tid": song[0]}})
            similarEdges = []
            weights = []

        print("getting all data end")

        return all_data

    # def main(self):
    #     print("getting nodes")
    #     nodes = self.get_all_nodes(self.lastfm_database)
    #     print("giving indexes")
    #     indexes = self.giving_indexes_to_tIds(nodes)

    #     print("getting all data")
    #     all_data = self.getting_all_data(self.lastfm_database, indexes)

    #     return all_data
