import signal
import tweepy
import sqlite3
from twittermoto import config, database

KEYWORDS = ['earthquake', 'terremoto', 'tembor', '地震', 'gempa bumi','lindol' , 'Lumilindol', 'lindu']
BLACKLIST = ['@Jasmine_Eq00', '@Rewrite_2011', '@RedneckBot']

run = True
class StreamListener(tweepy.StreamListener):

    def __init__(self, api=None):
        super(StreamListener, self).__init__(api)
        self.db = database.SQLite('tweets.db')


    def on_connect(self):
        """Called once connected to streaming server. """
        print('Streamer connected...')
        status_json = self.api.rate_limit_status()
        limit = status_json['resources']['application']['/application/rate_limit_status']['limit']
        remain = status_json['resources']['application']['/application/rate_limit_status']['remaining']
        print('Resources: {}/{}'.format(remain, limit))



    def on_status(self, status):
        global run
        """Called when a new status arrives"""
        if not prefilter(status):
            return run

        # print tweet
        print_status(status)

        # add tweet to database (tweets.db)
        if self.db.add(status):
            print('tweet {} saved to database.\n'.format(status.id))

        return run



    def on_error(self, status_code):
        """Called when a status code is returned"""
        print('An error occured in the Tweepy Twitter Streamer: {}'.format(status_code))
        return False



def interrupt_handler(signal, frame):
    '''
    This function is called when this script is interupted and terminated with
    a 'ctrl + c' command.
    '''
    global run
    print("Exiting after next tweet...")
    run = False



def prefilter(status):
    ''' prefilters a tweet status to see if it is suitable for twittermoto.
    Return value: True if the tweet passes the prefilter. False otherwise'''
    text        = status.text
    screen_name = '@' + status.user.screen_name
    # Ignore users on BLACKLIST
    if screen_name in BLACKLIST:
        return False
    # Ignore retweets.
    if text.startswith('RT'):
        return False
        # ensure at least one keyword is in tweet text.
    elif not any(kw in text for kw in KEYWORDS):
        return False
        # Ignore tweets with web links (http) and replies (@).
    elif any(kw in text for kw in ['http', '@']):
        return False
    else:
        return True


def print_status(status):
    ''' Prints a twitter status to the console'''
    out = '''@{}\n {} \n \
    geo data: {}\n Author location: {}\n time: {}'''.format(
    status.user.screen_name, status.text, status.geo,
    status.author.location, status.created_at)
    print(out)



if __name__ == '__main__':
    # Authenticate Twitter API
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)

    # Connect to Twitter API
    api = tweepy.API(auth, wait_on_rate_limit=True,
                           wait_on_rate_limit_notify=True)

    # Initialise tweet stream listener
    stream_listener = StreamListener(api)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

    # Add interupt function of program is terminated (ctrl + c)
    signal.signal(signal.SIGINT, interrupt_handler)

    # Begin streaming
    stream.filter(track=KEYWORDS)
    print('Exited.')
