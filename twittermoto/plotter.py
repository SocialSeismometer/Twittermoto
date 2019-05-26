from twittermoto import database
from twittermoto.detectionAlgorithm import DetectionAlgorithm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import requests
from datetime import datetime
from dateutil import parser


def get_data(db_filename, dt=60):
    db = database.SQLite(db_filename)
    time, tweet_freq = db.binned_count(dt=dt)
    db.close()

    DAs = [
        DetectionAlgorithm(2, 5, dt  =dt),
        DetectionAlgorithm(4, 10, dt =dt),
        DetectionAlgorithm(19, 9, dt =dt)
           ]


    C_t  = [[] for i in range(len(DAs))]

    # loop through tweet frequency data to simulate realtime measurements
    for t, tf in zip(time, tweet_freq):
        for i, DA in enumerate(DAs):
            C_t[i].append(DA(t, tf))

    # Query USGS for historical seismic data
    url      = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.csv'
    response = requests.get(url)
    data     = response.content.decode()
    df       = pd.read_csv(pd.compat.StringIO(data))

    return time, tweet_freq, C_t, DAs, df




def plot_tweetcount_vs_time(ax, time, tweet_freq):
    ax.plot(time, tweet_freq, 'k', lw=1.5)



def plot_USGS(ax, df):
    for i, row in df.iterrows():
        time_ref = parser.parse(row.time)
        if row.mag>5:
            ax.axvline(time_ref, lw=1, ls='--', c='r')
        elif row.mag>4:
            ax.axvline(time_ref, lw=0.5, ls='--', c='0.3')




def plot_detection_vs_time(ax, time, C_t):
    DA_labels = ['sensative', 'moderate', 'conservative']
    for i, ct in enumerate(C_t):
        ax.plot(time, ct, label=DA_labels[i])
    ax.axhline(1, ls='--', lw=1, c='k')




def plot_detection_region(ax, DA):
    for ts, te in DA.detections:
        ax.axvspan(ts, te, alpha=0.5, color='cyan')
