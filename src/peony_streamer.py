import asyncio
from twittermoto import config, settings, database, DetectionAlgorithm
from peony import PeonyClient
import peony
from datetime import datetime
import sqlite3

loop = asyncio.get_event_loop()
# create the client using your api keys
client = PeonyClient(config.consumer_key, config.consumer_secret,
config.access_token, config.access_token_secret)

DAs = [DetectionAlgorithm(2, 5),
       DetectionAlgorithm(4, 10),
       DetectionAlgorithm(19, 9)]

DB = database.SQLite('tweets.db')

async def track(queue):
    req = client.stream.statuses.filter.post(track=settings.KEYWORDS)
    # req is an asynchronous context
    async with req as stream:
        # stream is an asynchronous iterator
        async for tweet in stream:
            # check that you actually receive a tweet
            if peony.events.tweet(tweet):
                # you can then access items as you would do with a
                # `PeonyResponse` object
                if not prefilter(tweet):
                    continue

                print_status(tweet)

                add_status = DB.add(tweet.id, tweet.user.screen_name, tweet.text,
                               tweet.created_at, tweet.user.location)
                if add_status:
                    print('tweet {} saved to database.\n'.format(tweet.id))

                await queue.put(tweet)



def prefilter(status):
    ''' prefilters a tweet status to see if it is suitable for twittermoto.
    Return value: True if the tweet passes the prefilter. False otherwise'''
    text        = status.text
    screen_name = '@' + status.user.screen_name
    # Ignore users on BLACKLIST
    if screen_name in settings.BLACKLIST:
        return False
    # Ignore retweets.
    elif text.startswith('RT'):
        return False
    # ensure at least one keyword is in tweet text.
    elif not any(kw in text for kw in settings.KEYWORDS):
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
    status.user.location, status.created_at)
    print(out)




async def pop_queue(queue):
    count = 0
    while not queue.empty():
        tweet = queue.get_nowait()
        #print(tweet)
        count += 1
        #queue.task_done()
    detection = [DA(count) for DA in DAs]
    if any(x >= 1 for x in detection):
        print(datetime.now(), ', '.join([f'{x:2.2f}' for x in detection]))
    return

async def consume(queue):
    while True:
        await asyncio.gather(pop_queue(queue), asyncio.sleep(5))





if __name__ == '__main__':
    # run the coroutine
    queue = asyncio.Queue(loop=loop)
    loop.create_task(track(queue))
    loop.create_task(consume(queue))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Exited.')
