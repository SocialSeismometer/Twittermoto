import tweepy
from twittermoto import config

class StreamListener(tweepy.StreamListener):

    def on_connect(self):
        """Called once connected to streaming server.
        This will be invoked once a successful response
        is received from the server. Allows the listener
        to perform some work prior to entering the read loop.
        """
        print('Streamer connected...')
        status_json = self.api.rate_limit_status()
        limit = status_json['resources']['application']['/application/rate_limit_status']['limit']
        remain = status_json['resources']['application']['/application/rate_limit_status']['remaining']
        print(f'Resources: {remain}/{limit}')


    def on_status(self, status):
        """Called when a new status arrives"""
        #print(status)
        out = f'''@{status.user.screen_name}\n {status.text} \n \
geo data: {status.geo}\n time: {status.created_at}\n'''
        print(out)



    def on_error(self, status_code):
        """Called when a non-200 status code is returned"""
        if status_code == 420:
            return False


if __name__ == '__main__':

    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                           wait_on_rate_limit_notify=True)


    stream_listener = StreamListener(api)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=['earthquake', 'terremoto', 'tembor', '地震', 'gempa bumi','lindol' , 'lindu'])
