import os

import mysql.connector
from flask import app, g


def getdb():
    if 'db' not in g or not g.db.is_connected():
        g.db = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_DATABASE'),
        )
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None and db.is_connected():
        db.close()


#app.teardown_appcontext(close_db)