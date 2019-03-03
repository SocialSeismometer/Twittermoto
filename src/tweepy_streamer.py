import tweepy
from twittermoto import config, StreamListener




if __name__ == '__main__':

    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                           wait_on_rate_limit_notify=True)


    stream_listener = StreamListener(api)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=['earthquake', 'terremoto', 'tembor', '地震', 'gempa bumi','lindol' , 'lindu'])
