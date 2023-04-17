import utils
import json

connection = utils.connect_to_db('hgcentral')
dbDb = utils.get_table('dbDb', connection)

db = utils.find_tables_for('Human')[0]
connection = utils.connect_to_db(db)
genome_tables = utils.get_table_names(connection)
genome = utils.get_table(genome_tables[0], connection)

for gene in genome:
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


sequence = utils.to_list(genome[2])
print(sequence)