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
    print(f'Found {len(result)} tables for this genome')
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

def find_tables_for(organism):
    '''Find a table fot a specific genome e.g. "Human" in the current database'''
    connection = connect_to_db('hgcentral')
    gene_tables = []
    for item in get_table('dbDb', connection):
        
        if item['organism'] == organism or item['organism'].lower() == organism:
            gene_tables.append(item['name'])

    print(f'Found {len(gene_tables)} tables for {organism}: {gene_tables}')
    return gene_tables

def get_array(gene):
    '''Convert a gene from starts and lengths to binary list'''
    gene_start = gene['tStart']
    gene_end = gene['tEnd']
    exon_starts = gene['tStarts']
    exon_lengths = gene['blockSizes']
    if type(exon_starts) == int:
        exon_starts = [exon_starts]
    if type(exon_lengths) == int:
        exon_lengths = [exon_lengths]

    gene_length = gene_end - gene_start
    gene_array = [0] * gene_length

    for index, exon_start in enumerate(exon_starts):
        exon_length = exon_lengths[index]
        for i in range(exon_start, exon_start + exon_length):
            if gene_start <= i < gene_end:
                gene_array[i - gene_start] = 1

    return gene_array


def format_gene(gene):
    '''Format gene data into a dictionary with ints and lists for castable strings'''
    var_keys = list(gene.keys())
    for key in var_keys:
        gene[key] = str(gene[key]).replace("b'", '').replace(",'", '')
        if ',' in gene[key]:
            gene[key] = gene[key].split(',')
        try:
            if type(gene[key]) == list:
                for i in range(len(gene[key])):
                    gene[key][i] = int(gene[key][i])
            else:
                gene[key] = int(gene[key])
        except: ValueError 
        pass

    return gene