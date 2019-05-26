'''
This module contains the database classes.
'''
import sqlite3
from datetime import datetime

class database(object):
    "A base class for a tweet database"

    def __init__(self, *args):
        pass

    def __len__(self):
        pass

    # def connect(self):
    #     pass



    def close(self):
        pass

    def add(self, status):
        pass


class SQLite(database):
    "A class for a tweet database in SQLite"

    time_ranges = {
    'hour': '\'-1 Hour\'',
    'day': '\'-1 day\'',
    'week': '\'-7 days\'',
    'month': '\'-1 month\'',
    'year': '\'-1 year\'',
    'all': '\'-100 years\'', # assumes no tweets older than a century.
    }
    def __init__(self, filename):
        sql_create_table = """CREATE TABLE IF NOT EXISTS tweets (
                                        id INTEGER PRIMARY KEY,
                                        screen_name TEXT,
                                        text TEXT,
                                        created_at DATE,
                                        location TEXT,
                                        text_trans TEXT,
                                        lat DOUBLE,
                                        long DOUBLE
                                    );"""
        self.conn = sqlite3.connect(filename)
        self.conn.execute(sql_create_table)



    def __len__(self):
        out = self.query('SELECT COUNT(*) FROM tweets')
        return next(out)[0]


    def close(self):
        self.conn.close()

    def add(self, id, screen_name, text, created_at, location):
        sql_insert = '''INSERT OR REPLACE INTO tweets(id, screen_name, text, created_at, location, text_trans, lat, long)
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?)'''
        data = [id, '@' + screen_name, text, created_at, location, None, None, None]
        self.conn.execute(sql_insert, data)
        self.conn.commit()
        return True

    def update(self, id, **kwargs):
        """updates fields in a single row of the tweets database. Fields to update
        and their corresponding value are passed as dictionary key-value pairs.

        Args:
            id       (int): Identification number of the tweet.
            kwargs    (dict): the keys are the field to update, and the values
                              are the value to update that field.


        Returns:
            bool: True for success, False otherwise.
        """
        to_set = ', '.join('{} = ?'.format(k) for k, v in kwargs.items())
        values = [x for x in kwargs.values()] + [id]
        sql = ''' UPDATE tweets
                         SET {}
                         WHERE id = ?'''.format(to_set)

        try:
            self.conn.execute(sql, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_tweets(self, timerange='all'):
        the_query = 'SELECT * FROM tweets \
        WHERE datetime(created_at) > datetime(\'now\', {})'.format(self.time_ranges[timerange])

        yield from self.query(the_query)


    def binned_count(self, dt=5, timerange='all'):
        the_query = f'''SELECT STRFTIME(\'%s\',created_at)/{dt} as time_column, COUNT(*)
        FROM tweets
        WHERE datetime(created_at) >= datetime('now', '-100 years')
        GROUP BY time_column'''

        X, Y = [], []
        oldValue , diffValue = [] , []
        for i, newValue in enumerate(self.query(the_query)):
            if i == 0:
                X.append(datetime.utcfromtimestamp(newValue[0]*dt))
                Y.append(newValue[1]*60/dt)
            else:
                diffValue = newValue[0] - oldValue[0]
                if diffValue > 1:
                    for j in range(diffValue):
                        X.append(datetime.utcfromtimestamp((oldValue[0] + j + 1)*dt))
                        if j == diffValue-1:
                            Y.append(newValue[1])
                        else:
                            Y.append(0)
                else:
                    X.append(datetime.utcfromtimestamp(newValue[0]*dt))
                    Y.append(newValue[1]*60/dt)
            oldValue = newValue
        return X, Y


    def query(self, the_query):
        cur = self.conn.cursor()
        cur.execute(the_query)
        rows = cur.fetchall()

        for row in rows:
            yield row
