from twittermoto import Streamer, config


auth = {
    'consumer_key'        :config.consumer_key,
    'consumer_secret'     :config.consumer_secret,
    'access_token'        :config.access_token,
    'access_token_secret' :config.access_token_secret
}

keywords = ['earthquake', 'terremoto', 'temblor', '地震', 'jishin', 'gempa bumi','aardbeving',
            'lindol', 'Lumilindol', 'lindu', 'zemljotres', 'sismo', 'زلزال', 'زلزلہ']

streamer = Streamer(auth_keys=auth,
                    filename='tweets.db',
                    keywords=keywords)

streamer.stream()
