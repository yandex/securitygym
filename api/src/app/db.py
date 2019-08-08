import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask import g
from flask import current_app

from app import settings


def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            dbname=settings.DB_NAME
        )
        g.db.autocommit = True
    return g.db


def init_db():
    raw_db = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
    raw_db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = raw_db.cursor()
    cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = %s", (settings.DB_NAME,))
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("CREATE DATABASE %s" % settings.DB_NAME)
        raw_db.commit()
        raw_db.close()
    db = get_db()
    cursor = db.cursor()
    with current_app.open_resource('schema.sql') as f:
        cursor.execute(f.read().decode('UTF-8'))
    db.commit()
