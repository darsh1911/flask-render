import os
import pymysql.cursors


def getdb():
    connection = pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_DATABASE'),
    )
    return connection


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None and db.is_connected():
        db.close()