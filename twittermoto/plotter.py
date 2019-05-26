from twittermoto import database, detectionAlgorithm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import requests
from datetime import datetime
from dateutil import parser


def plot_detector_vs_time(db_filename, dt=5):
    # Query data from tweet database.
    db = database.SQLite(db_filename)
    time, tweet_freq = detectionAlgorithm.get_tweet_frequency(db, dt=dt)

    DAs = [detectionAlgorithm.DetectionAlgorithm(2, 5, dt=dt),
           detectionAlgorithm.DetectionAlgorithm(4, 10, dt=dt),
           detectionAlgorithm.DetectionAlgorithm(19, 9, dt=dt)]
    DA_labels = ['sensative', 'moderate', 'conservative']

    C_t = x = [[] for i in range(len(DAs))]

    # loop through tweet frequency data to simulate realtime measurements
    for tf in tweet_freq:
        # update each detection algorithm with current tweet frequency
        for i, DA in enumerate(DAs):
            C_t[i].append(DA(tf))

    # Query USGS for historical seismic data
    url      = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.csv'
    response = requests.get(url)
    data     = response.content.decode()
    df       = pd.read_csv(pd.compat.StringIO(data))


    # Plot
    fig, axes = plt.subplots(2, 1, sharex=True)


    axes[0].set_ylabel('Earthquake\ntweets per minute')
    axes[1].set_ylabel('Detection\nfunction')
    axes[0].plot(time, tweet_freq)
    for i, ct in enumerate(C_t):
        axes[1].plot(time, ct, label=DA_labels[i])

    # plot reference data
    for i, row in df.iterrows():
        time_ref = parser.parse(row.time)
        if row.mag>5:
            axes[0].axvline(time_ref, lw=1, ls='--', c='r')
            axes[1].axvline(time_ref, lw=1, ls='--', c='r')
        elif row.mag>4:
            axes[0].axvline(time_ref, lw=0.5, ls='--', c='0.3')
            axes[1].axvline(time_ref, lw=0.5, ls='--', c='0.3')
    axes[1].axhline(1, ls='--', lw=1, c='k')
    axes[1].set_ylim(0, 2)
    axes[1].set_xlim(min(time), max(time))
    axes[1].legend()
    fig.autofmt_xdate()
    myFmt = mdates.DateFormatter('%d-%b %H:%M')
    axes[1].xaxis.set_major_formatter(myFmt)

    return fig




def plot_tweetcount_vs_time(db_filename, dt=600):
    the_query = 'SELECT STRFTIME(\'%s\', created_at)/{} as minute, COUNT(*) \
    FROM tweets GROUP BY minute'.format(dt)

    # Query data from database.
    db = database.SQLite(db_filename)
    X, Y = [], []
    for i, row in enumerate(db.query(the_query)):
        X.append(datetime.utcfromtimestamp(row[0]*dt))
        Y.append(row[1])
    db.close()

    # Query USGS for historical seismic data
    url      = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.csv'
    response = requests.get(url)
    data     = response.content.decode()
    df       = pd.read_csv(pd.compat.StringIO(data))


    # Plot data
    fig = plt.figure()

    plt.plot(X, Y, 'k', lw=1.5)
    for i, row in df.iterrows():
        time = parser.parse(row.time)
        if row.mag>5:
            plt.axvline(time, lw=1, ls='--', c='r')
        elif row.mag>4:
            plt.axvline(time, lw=0.5, ls='--', c='0.3')

    # prettify date on x-axis
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%d-%b %H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)

    plt.ylabel('Earthquake tweet rate [tweets/10 min]')
    plt.xlim(min(X), max(X))
    plt.ylim(0, max(Y))

    return fig
