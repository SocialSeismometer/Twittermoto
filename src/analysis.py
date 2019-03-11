import os
from twittermoto import database
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_tweetcount_vs_time(db, dt=600):
    the_query = f'SELECT STRFTIME(\'%s\', created_at)/{dt} as minute, COUNT(*) \
    FROM tweets GROUP BY minute'


    X, Y = [], []
    for i, row in enumerate(db.query(the_query)):
        X.append(datetime.fromtimestamp(row[0]*dt))
        Y.append(row[1])

    plt.figure()
    plt.plot(X, Y)

    # prettify date on x-axis
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%d-%b %H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)

    plt.ylabel(f'Earthquake tweet rate [tweets/10 min]')
    plt.ylim(0, max(Y))
    plt.savefig('fig/tweetcount_vs_time.png', dpi=200)



def plot_top_tweeters(db, N=20):
    the_query = f'SELECT screen_name, COUNT(*) as count FROM tweets \
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
