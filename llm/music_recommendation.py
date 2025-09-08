import pandas as pd
from urllib import request
from pathlib import Path
from datetime import datetime

base_dir = Path(__file__).resolve().parent
data_path = base_dir / "data" / "train.txt"
data = open(str(data_path), "rb")
lines = data.read().decode("utf-8").split('\n')[2:]

playlists = [s.rstrip().split() for s in lines if len(s.split()) > 1]

songs_path = base_dir / 'data' / 'song_hash.txt'
songs_file = open(str(songs_path), 'rb')
songs_file = songs_file.read().decode("utf-8").split('\n')
songs = [s.rstrip().split('\t') for s in songs_file]
songs_df = pd.DataFrame(data=songs, columns = ['id', 'title', 'artist'])
songs_df = songs_df.set_index('id')

print('Playlist #1:\n', playlists[0], '\n')
print('Playlist #2:\n', playlists[1])

print("start training model at ", datetime.now())
from gensim.models import Word2Vec
model = Word2Vec(sentences=playlists, vector_size=32, window=20, negative=50, min_count=1, workers=4)
print("model trained at ", datetime.now())

song_id = 2172
similar_songs = model.wv.most_similar(positive=str(song_id))

print(f"Song ID: {song_id}")
print(f"Song Title: {songs_df.iloc[song_id]['title']}")
print(f"Similar Songs: {similar_songs}")

import numpy as np
def print_recommendations(song_id):
    similar_songs = np.array(model.wv.most_similar(positive=str(song_id), topn=5))[:,0]
    return songs_df.iloc[similar_songs]

print(print_recommendations(song_id))
