# Important Libraries
import streamlit as st
import pandas as pd
import random
import numpy as np

#Visualisation
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Data Processing
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Unsupervised ML
from sklearn.cluster import KMeans
from matplotlib.lines import Line2D
from sklearn.metrics import silhouette_score

# Spotify API Related
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import CLIENT_ID, CLIENT_SECRET


# Importing Datasets
billboard_df = pd.read_csv("billboard_df.csv")
Whole_df = pd.read_csv("whole_df.csv")

# Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,client_secret=CLIENT_SECRET))
def play_song(track_id):
    st.components.v1.iframe(
        src=f"https://open.spotify.com/embed/track/{track_id}",
        width=320,
        height=80,
        scrolling=False
    )


# Streamlit app
def song_recommender():
    
    st.title("🎵 Song Recommender")
    trending_choice = st.selectbox("Are you interested in a Trending Now song?", ["Select a choice", "Yes", "No"])

    if trending_choice == "Yes":
        recommended_song = random.choice(billboard_df['Song'])
        artist = billboard_df.loc[billboard_df["Song"] == recommended_song, 'Artist'].values[0]
        number = billboard_df.loc[billboard_df["Song"] == recommended_song, 'Number'].values[0]

        st.success(f"We recommend you this awesome song: **{recommended_song}** by **{artist}** 🎤")
        st.info(f"It’s currently number {number} on the Billboard Hot 100!")

        song_id = sp.search(q=recommended_song, type='track', market="GB")["tracks"]["items"][0]["id"]
        play_song(song_id)

    elif trending_choice == "No":
        st.warning("Maybe you are just not cool enough 😎")

        label = st.selectbox(
            "Don't worry, choose a genre/mood cluster:",
            options=[0, 1, 2, 3, 4, 5],
            format_func=lambda x: f"Cluster {x}"  # TODO: replace with genre names
        )

        if st.button("Recommend me songs!"):
            filtered_data = Whole_df[Whole_df['Labels'] == label]
            track_ids = random.sample(filtered_data['track_id'].tolist(), 3)

            for tid in track_ids:
                play_song(tid)

song_recommender()