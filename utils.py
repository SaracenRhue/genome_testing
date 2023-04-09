import pymysql
import json


def connect_to_db(db='hgcentral'):
    '''Connect to the MySQL server and return a connection object'''
    connection = pymysql.connect(
        host='genome-euro-mysql.soe.ucsc.edu',
        port=3306,
        user='genome',
        db=db,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


def get_table_names(connection):
    '''Get a list of table names in the current database'''
    cursor = connection.cursor()
    sql = 'SHOW TABLES'
    cursor.execute(sql)
    tables = cursor.fetchall()
    cursor.close()
    result = []
    for table in tables:
        result.append(list(table.values())[0])
    return result

def to_json(table, connection):
    '''Convert a table to JSON'''
    cursor = connection.cursor()
    sql = f'SELECT * FROM {table}'
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    with open(f'{table}.json', 'w') as f:
        json.dump(data, f)
    cursor.close()
    connection.close()

def get_table(table, connection):
    '''Get the data from a table'''
    cursor = connection.cursor()
    sql = f'SELECT * FROM {table}'
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    cursor.close()
    return data

def find_table_for(organism):
    '''Find a table in the current database'''
    connection = connect_to_db('hgcentral')
    for item in get_table('dbDb', connection):
        if item['organism'] == organism or item['organism'].lower() == organism:
            return item['name']
    return 'none found'