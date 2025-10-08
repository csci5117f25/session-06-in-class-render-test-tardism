""" database access
docs:
* https://www.psycopg.org/psycopg3/docs/advanced/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from contextlib import contextmanager
import logging
import os

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

def add_survey_response(text_input, radio_choice, select_choice, checkbox, textarea_input):
    with get_db_cursor(True) as cur:
        current_app.logger.info("Adding survey response")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS survey_responses (
                id SERIAL PRIMARY KEY,
                text_input TEXT NOT NULL,
                radio_choice TEXT NOT NULL,
                select_choice TEXT NOT NULL,
                checkbox BOOLEAN NOT NULL,
                textarea_input TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            INSERT INTO survey_responses
            (text_input, radio_choice, select_choice, checkbox, textarea_input)
            VALUES (%s, %s, %s, %s, %s)
        """, (text_input, radio_choice, select_choice, checkbox, textarea_input))

def get_survey_results(reverse=False):
    with get_db_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS survey_responses (
                id SERIAL PRIMARY KEY,
                text_input TEXT NOT NULL,
                radio_choice TEXT NOT NULL,
                select_choice TEXT NOT NULL,
                checkbox BOOLEAN NOT NULL,
                textarea_input TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        order = "DESC" if reverse else "ASC"
        cur.execute(f"SELECT * FROM survey_responses ORDER BY id {order}")
        rows = cur.fetchall()

        results = []
        for row in rows:
            results.append({
                'id': row['id'],
                'text_input': row['text_input'],
                'radio_choice': row['radio_choice'],
                'select_choice': row['select_choice'],
                'checkbox': row['checkbox'],
                'textarea_input': row['textarea_input'],
                'timestamp': row['timestamp'].isoformat() if row['timestamp'] else None
            })
        return results
