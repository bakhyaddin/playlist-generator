import os
import sys
import sqlite3

from preprocessing import Preprocessing

preprocessingClass = Preprocessing("lastfm_similars.db")
nodes = preprocessingClass.get_all_nodes()
indexes = preprocessingClass.giving_indexes_to_tIds(nodes)
allData = preprocessingClass.getting_all_data(indexes)

allDataTrackIds = []

for node in allData:
    allDataTrackIds.append(allData[node]["tid"])



outFile = open('track_list.txt','w')
conn = sqlite3.connect("track_metadata.db")
cur = conn.cursor()
cur.execute("SELECT track_id, title, artist_name FROM songs")
while True:
    song = cur.fetchone()
    if not song:
        break
    track_id = song[0]
    title = song[1]
    astist_name = song[2]
    if(track_id in allDataTrackIds):
        ss = '%s<S>%s<S>%s\n' % (track_id, astist_name, title)
        outFile.write(ss)
conn.close()
