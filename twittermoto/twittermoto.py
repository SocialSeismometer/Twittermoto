import tweepy
from twittermoto import config
import time


def run():
    if config.access_token is None:
        print('You haven''t set your Twitter access tokens yet. Please store your access tokens in config.py')
        return
        
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)


    print("Jaime's Twitter Earthquake Detector. Initialising...")
    api = tweepy.API(auth, wait_on_rate_limit=True,
                       wait_on_rate_limit_notify=True)


    #Check how many searches you have remaining (usually you get 180 per 15 minutes)
    searchesRemaining = api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']
    print('Searches Remaining: ', searchesRemaining)

    lastID = api.search("earthquake",rpp=1).pop().id
    LMA = 1
    SMA = 0
    hist = [9]*240
    while True:
        startTime = time.time()
        count = 0
        geoCount = 0

        for i,tweet in enumerate(tweepy.Cursor(api.search,q="earthquake OR terremoto OR tembor OR 地震 OR \"gempa bumi\" OR lindol OR lindu",since_id=lastID,rpp=100).items(200)):
            if SMA/LMA > 10:
                print(time.strftime("%H:%M:%S: ", time.localtime(startTime)), tweet.text)
            if i == 0: lastID = tweet.id
            count = i
            if tweet.geo:
                geoCount += 1
                lastGeo = tweet.geo
                #print(tweet.geo['coordinates'])

        hist = [count] + hist[0:239]
        LMA = sum(hist)/60.0
        SMA = sum(hist[0:4])
        #if count > 0:
            #print(time.strftime("%H:%M:%S: ", time.localtime(startTime)),'There were ',count,' earthquake tweets, ',geoCount,' with geographic data')
        #print('LMA: ', LMA, ' SMA: ',SMA,' SMA/LMA: ',SMA/LMA)
        print(count, round(SMA/LMA,2))
        
        if time.time()-startTime < 15:
            time.sleep(15 - (time.time()-startTime))
        

    print('End.')
