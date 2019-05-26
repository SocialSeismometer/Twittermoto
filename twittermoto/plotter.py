from twittermoto import database
from twittermoto.detectionAlgorithm import DetectionAlgorithm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta
from dateutil import parser
from collections import namedtuple
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

DataClass = namedtuple('DataClass', ['time', 'tweet_freq', 'detection_func', 'DAs', 'USGS'])

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

    return DataClass(time, tweet_freq, C_t, DAs, df)


def list_detections(data):
    detections = []

    # Assumption: the sensitive algorithm will always be the first algorithm to detect.
    for TS, TE in data.DAs[0].detections:

        this_detection = [TS, TE, 1, False] # starttime, endtime, confidence
        for i, DA in enumerate(data.DAs[1:]):
            for ts, te in DA.detections:
                if (ts>=TS) and (ts<=TE):
                    this_detection[2] += 1
        detections.append(this_detection)


    data.USGS['time_parsed'] = [parser.parse(x, ignoretz=True) for x in data.USGS.time]

    # print()
    for i, d in enumerate(detections):
        nearby_detections = data.USGS[abs((data.USGS.time_parsed - d[0])) <= timedelta(minutes=5)]
        if len(nearby_detections) > 0:
            detections[i][3] = True

    confidence_choices = {1:'Low', 2:'Medium', 3:'High'}
    for i in range(len(detections)):
        detections[i][2] = confidence_choices[detections[i][2]]

    out = pd.DataFrame(detections, columns = ['time', 'end_time', 'confidence', 'confirmed'])
    out = out.sort_values('time', ascending=False)
    return out



def plot_tweetcount_vs_time(ax, data):
    ax.plot(data.time, data.tweet_freq, 'k', lw=1.5)



def plot_USGS(ax, data):
    for i, row in data.USGS.iterrows():
        time_ref = parser.parse(row.time)
        if row.mag>5:
            ax.axvline(time_ref, lw=1, ls='--', c='r')
        elif row.mag>4:
            ax.axvline(time_ref, lw=0.5, ls='--', c='0.3')




def plot_detection_vs_time(ax, data):
    DA_labels = ['sensative', 'moderate', 'conservative']
    for i, ct in enumerate(data.detection_func):
        ax.plot(data.time, ct, label=DA_labels[i])
    ax.axhline(1, ls='--', lw=1, c='k')




def plot_detection_region(ax, data, ind=0):
    for ts, te in data.DAs[ind].detections:
        ax.axvspan(ts, te, alpha=0.5, color='cyan')
