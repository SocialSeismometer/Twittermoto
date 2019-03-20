# Set your access tokens here. 
# NEVER commit this file. 
#NEVER publish your private keys and tokens.

consumer_key        = None
consumer_secret     = None
access_token        = None
access_token_secret = None
if any(x is None for x in [consumer_key, consumer_secret, access_token, access_token_secret]):
    raise ValueError('Twitter API access tokens not found. Did you put your API data in twittermoto.config?')
