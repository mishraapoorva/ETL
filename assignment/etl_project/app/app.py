from flask import Flask
import petl as etl
from sqlalchemy import create_engine
import sys
import pymysql

def get_full_name(record):
    return record['first_name'] + ' ' + record['last_name']

def get_company_name(record):
    parts = record['email'].split('@')
    if len(parts) >= 1:
        return parts[1]
    else:
        return ''

class CursorProxy(object):
     def __init__(self, cursor):
         self._cursor = cursor
     def executemany(self, statement, parameters, **kwargs):
         # convert parameters to a list
         parameters = list(parameters)
         # pass through to proxied cursor
         return self._cursor.executemany(statement, parameters, **kwargs)
     def __getattr__(self, item):
         return getattr(self._cursor, item)

def get_cursor(connection):
     return CursorProxy(connection.cursor())

print('starting etl server', file=sys.stdout)

app = Flask(__name__)

@app.route('/')
def default():
    return 'Hello World!'

@app.route('/mongo')
def mongo_etl():
    print("Inside mongo", file=sys.stdout)
    return 'Mongo ETL Completed'

@app.route('/mysql')
def mysql_etl():
    try:
        print("extracting csv data", file=sys.stdout)
        data = etl.fromcsv('DATA.csv')
        print("tranforming data", file=sys.stdout)
        data = etl.addfield(data, 'full_name', lambda record: get_full_name(record))
        data = etl.addfield(data, 'company', lambda record: get_company_name(record))
        print("loading data to mysql", file=sys.stdout)
        engine = create_engine('mysql+pymysql://root:root_password_123@172.31.14.230/sfl')
        connection = engine.raw_connection()
        connection.cursor().execute('SET SQL_MODE=ANSI_QUOTES')
        connection.cursor().execute('DROP TABLE IF EXISTS users;')
        etl.todb(data, get_cursor(connection) , 'users', create=True)
        return 'MySQL ETL Completed'
    except Exception as error:
        print("etl for mysql has error", file=sys.stdout)
        print('error message: {}'.format(error), file=sys.stdout)
        return str(error)

