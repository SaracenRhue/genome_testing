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



def create_matrix(variants):
    # Determine the length of the longest variant
    longest_variant_length = max(
        variant['txEnd'] - variant['txStart'] for variant in variants
    )

    # Determine the earliest start point of all variants
    earliest_start = min(
        variant['txStart'] for variant in variants
    )

    # Create matrix
    matrix = []
    for variant in variants:
        if type(variant['exonStarts']) == int:
            variant['exonStarts'] = [variant['exonStarts']]
        if type(variant['exonEnds']) == int:
            variant['exonEnds'] = [variant['exonEnds']]
        # Initialize an array filled with zeros
        variant_array = [0] * (longest_variant_length + earliest_start)

        for i in range(len(variant['exonStarts'])):
            # Offset the start and end points by the earliest start point
            exon_start = variant['exonStarts'][i] - earliest_start
            exon_end = variant['exonEnds'][i] - earliest_start

            for j in range(exon_start, exon_end):
                variant_array[j] = 1

        matrix.append(variant_array)

    return matrix



