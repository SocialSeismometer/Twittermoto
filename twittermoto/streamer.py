import signal
import tweepy
import sqlite3
from twittermoto import database


RUN = True

def interrupt_handler(signal, frame):
    '''
    This function is called when this script is interupted and terminated with
    a 'ctrl + c' command.
    '''
    global RUN
    print("Exiting after next tweet...")
    RUN = False

# Add interupt function of program is terminated (ctrl + c)
signal.signal(signal.SIGINT, interrupt_handler)


class Streamer(tweepy.Stream):

    def __init__(self, auth_keys=None, filename='tweets.db', keywords=[], user_blacklist=[]):
        self.keywords = keywords
        # Authenticate Twitter API
        auth = tweepy.OAuthHandler(auth_keys['consumer_key'], auth_keys['consumer_secret'])
        auth.set_access_token(auth_keys['access_token'], auth_keys['access_token_secret'])

        # Connect to Twitter API
        api = tweepy.API(auth, wait_on_rate_limit=True,
                               wait_on_rate_limit_notify=True)

        # Initialise tweet stream listener
        stream_listener = StreamListener(api, filename, keywords, user_blacklist)
        super(Streamer, self).__init__(auth=api.auth, listener=stream_listener)



    def stream(self):
        self.filter(track=self.keywords)





class StreamListener(tweepy.StreamListener):

    def __init__(self, api, filename, keywords=[], user_blacklist=[]):
        self.keywords = keywords
        self.user_blacklist = user_blacklist
        self.db = database.SQLite(filename)

        super(StreamListener, self).__init__(api)


    def on_connect(self):
        """Called once connected to streaming server. """
        print('Streamer connected...')
        status_json = self.api.rate_limit_status()
        limit = status_json['resources']['application']['/application/rate_limit_status']['limit']
        remain = status_json['resources']['application']['/application/rate_limit_status']['remaining']
        print('Resources: {}/{}'.format(remain, limit))



    def on_status(self, status):
        global RUN
        """Called when a new status arrives"""
        if not self.prefilter(status):
            return RUN

        # print tweet
        print_status(status)

        # add tweet to database
        add_status = self.db.add(status.id, status.user.screen_name, status.text,
                       status.created_at, status.author.location)
        if add_status:
            print('tweet {} saved to database.\n'.format(status.id))

        return RUN



    def on_error(self, status_code):
        """Called when a status code is returned"""
        print('An error occured in the Tweepy Twitter Streamer: {}'.format(status_code))
        return False


    def prefilter(self, status):
        ''' prefilters a tweet status to see if it is suitable for twittermoto.
        Return value: True if the tweet passes the prefilter. False otherwise'''
        text        = status.text
        screen_name = '@' + status.user.screen_name
        # Ignore users on BLACKLIST
        if screen_name in self.user_blacklist:
            return False
        # Ignore retweets.
        if text.startswith('RT'):
            return False
            # ensure at least one keyword is in tweet text.
        elif not any(kw in text for kw in self.keywords):
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
