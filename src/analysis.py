import os
from twittermoto import database
from datetime import datetime
from dateutil import parser
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz

def plot_tweetcount_vs_time(db, dt=600):
    the_query = 'SELECT STRFTIME(\'%s\', created_at)/{} as minute, COUNT(*) \
    FROM tweets GROUP BY minute'.format(dt)


    X, Y = [], []
    for i, row in enumerate(db.query(the_query)):
        X.append(datetime.utcfromtimestamp(row[0]*dt))
        Y.append(row[1])

    plt.figure()

    plt.plot(X, Y, 'k', lw=1.5)
    # plot historical seismic data
    url='https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.csv'
    response = requests.get(url)

    data = response.content.decode()
    df = pd.read_csv(pd.compat.StringIO(data))
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
    plt.savefig('fig/tweetcount_vs_time.png', dpi=200)



def plot_top_tweeters(db, N=20):
    the_query = 'SELECT screen_name, COUNT(*) as count FROM tweets \
    GROUP BY screen_name \
    ORDER BY count DESC\
    LIMIT 20'

    user, n_tweets = [], []
    for i, row in enumerate(db.query(the_query)):
        user.append(row[0])
        n_tweets.append(row[1])

    plt.figure()
    plt.title('Top Earthquake Tweeters')
    X = np.arange(len(user))
    plt.bar(X, n_tweets)
    plt.xticks(X, user, rotation=45,horizontalalignment='right')
    plt.ylabel('tweets')
    plt.tight_layout()
    plt.savefig('fig/top_tweeters.png', dpi=200)




if __name__ == '__main__':

    # Create target Directory if don't exist
    if not os.path.exists('fig'):
        os.mkdir('fig')

    db = database.SQLite('tweets.db')

    plot_tweetcount_vs_time(db)
    plot_top_tweeters(db)
    #plt.show()
