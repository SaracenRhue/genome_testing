from config import connection
import json
import yaml

def get_table_names(connection=connection):
    '''Get a list of table names in the current database'''
    cursor = connection.cursor()
    sql = 'SHOW TABLES'
    cursor.execute(sql)
    tables = cursor.fetchall()
    cursor.close()
    result = []
    for table in tables:
        result.append(table['Tables_in_hgcentral'])
    return result

def to_yaml(table, connection=connection):
    '''Convert a table to YAML'''
    cursor = connection.cursor()
    sql = f'SELECT * FROM {table}'
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    with open('data.yaml', 'w') as f:
        yaml.dump(data, f)
    cursor.close()
    connection.close()

def to_json(table, connection=connection):
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


