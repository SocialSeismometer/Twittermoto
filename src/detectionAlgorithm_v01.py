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

def STA_LTA_Detection(db, dt = 5):   # short term average and long term average detection algorithm
    the_query = f'SELECT STRFTIME(\'%s\',created_at)/{dt} as time_column, COUNT(*) \
    FROM tweets GROUP BY time_column'
    
    normConstant = 60/dt # constant for normalization to tweets per minute
    setSTA = 60          # setting short term average in seconds
    setLTA = 3600        # setting long term average in seconds
    mConstant = 19        # Constant for characteristic function, it defines the increased STA necessary to trigger at a larger LTA
    bConstant = 9       # Constant for characteristic function, it defines the STA value that will cause an event trigger when the LTA is zero
    
    # Data Conditioning to fill in missing time indices with zero tweets
    X, Y = [], [] 
    oldValue , diffValue = [] , []
    for i, newValue in enumerate(db.query(the_query)):
        if i == 0:
            X.append(datetime.fromtimestamp(newValue[0]*dt))
            Y.append(newValue[1])
        else:
            diffValue = newValue[0] - oldValue[0]
            if diffValue > 1:
                for j in range(diffValue):
                    X.append(datetime.fromtimestamp((oldValue[0] + j + 1)*dt))
                    if j == diffValue-1:
                        Y.append(newValue[1])
                    else:
                        Y.append(0)
            else:
                X.append(datetime.fromtimestamp(newValue[0]*dt))
                Y.append(newValue[1])                             
        oldValue = newValue
    Y = [y_tmp*normConstant for y_tmp in Y]   # normalizing Y list into tweets per minute 

    # Computing short term and long term averages
    X_STA , Y_STA = [] , []    
    X_LTA , Y_LTA = [] , []    
    for k in range(len(X)):
        if k >= int(setLTA/dt-1):
            X_STA.append( X[k] )
            Y_STA.append( sum(Y[(k-int(setSTA/dt)-1):k])/(setSTA/dt) )
            X_LTA.append( X[k] )
            Y_LTA.append( sum(Y[(k-int(setLTA/dt)-1):k])/(setLTA/dt) )
    
    # Computing characteristic function 
    X_CF , Y_CF = [] , []
    threshold_CF = []
    for l in range(len(X_STA)):
        X_CF.append( X_STA[l] )
        Y_CF.append( Y_STA[l]/(mConstant*Y_LTA[l] + bConstant) )
        threshold_CF.append(1)
        
    # Plotting "TweetGram"
    plt.figure()
    plt.plot(X, Y)     
    # prettify date on x-axis
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%d-%b %H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.ylabel(f'Earthquake tweet rate [tweets/min]')
    plt.ylim(0, max(Y))

    # Plotting STA and LTA
    plt.figure()
    plt.plot(X_STA, Y_STA,label = 'STA')
    plt.plot(X_LTA, Y_LTA,label = 'LTA')     
    # prettify date on x-axis
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%d-%b %H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.ylabel(f'Earthquake tweet rate [tweets/min]')
    plt.ylim(0, max(Y_STA))  
    plt.legend(loc='upper left')
  
    # Plotting Characteristic Function
    plt.figure()
    plt.plot(X_CF, Y_CF)
    plt.plot(X_CF, threshold_CF ,'--' , label='detection threshold')     
    # prettify date on x-axis
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%d-%b %H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.ylabel(f'Characteristic Function [-]')
    plt.ylim(0, max(Y_CF))      
    plt.legend(loc='upper left')
            
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
    STA_LTA_Detection(db)
