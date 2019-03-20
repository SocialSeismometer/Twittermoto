from twittermoto import database
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import time

if __name__ == '__main__':
    # load required objects
    db          = database.SQLite('tweets.db')
    geolocator  = Nominatim()
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


    query = '''SELECT id, STRFTIME(\'%s\', created_at)/60 as minute, location, lat, long
    from tweets'''

    for i, row in enumerate(db.query(query)):
        id, minute, location, lat, long = row

        if lat is None and location is not None:
            print('updating {}'.format(id))
            geo = geocode(location)

            if geo is not None:
                db.update(id, lat=geo.latitude, long=geo.longitude)
                print('coordinates found! ', geo.latitude, geo.longitude)
            else:
                print('no coordinates :(')
                db.update(id, location=None)
