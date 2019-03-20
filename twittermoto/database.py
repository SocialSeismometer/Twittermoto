'''
This module contains the database classes.
'''
import sqlite3


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

    def add(self, status):
        sql_insert = '''INSERT OR REPLACE INTO tweets(id, screen_name, text, created_at, location, text_trans, lat, long)
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?)'''
        data = [status.id, '@' + status.user.screen_name, status.text,
                status.created_at, status.author.location,
                None, None, None]
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



    def query(self, the_query):
        cur = self.conn.cursor()
        cur.execute(the_query)
        rows = cur.fetchall()

        for row in rows:
            yield row
