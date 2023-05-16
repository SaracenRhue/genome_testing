import utils
import json
import time
import utils

START_TIME = time.time()


connection = utils.connect_to_db('hgcentral')
dbDb = utils.get_table('dbDb', connection)

db = utils.find_tables_for('Human')[0]
connection = utils.connect_to_db(db)
genome_tables = utils.get_table_names(connection)


table = genome_tables.index('ncbiRefSeq')
genome = utils.get_table(genome_tables[table], connection)

genome = [utils.format_gene(gene) for gene in genome]
data = {}
for gene in genome: data[gene['name2']] = []
for gene in genome: data[gene['name2']].append(gene)
for gene in data: data[gene].sort(key=lambda x: x['exonCount'])
for gene in data:
    length = data[gene][0]['txEnd'] - data[gene][0]['txStart']

        
for gene in data:
    for variant in data[gene]:
        variant.pop('bin')
        variant.pop('chrom')
        variant.pop('strand')
        variant.pop('cdsStart')
        variant.pop('cdsEnd')
        variant.pop('score')
        variant.pop('name2')
        variant.pop('cdsStartStat')
        variant.pop('cdsEndStat')
        variant.pop('exonFrames')

new_data = []
data_keys = list(data.keys())

for key in data_keys:
    data[key] = {
        'name': key,
        'variants': data[key], 
        'matrix': []
    }
    new_data.append(data[key])

    
for gene in new_data:
    gene['matrix'] = utils.create_matrix({'variants': gene['variants']})['matrix']


with open('out.json', 'w') as f:
    json.dump(data, f, indent=4)

END_TIME = time.time()
print(f'Time taken: {int(END_TIME - START_TIME)}s')
