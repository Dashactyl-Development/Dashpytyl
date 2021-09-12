import sqlite3
from sqlite3.dbapi2 import Cursor


def db_create():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS main(
            id text,
            username text
            )
            ''')

  