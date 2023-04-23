import utils
import json

connection = utils.connect_to_db('hgcentral')
dbDb = utils.get_table('dbDb', connection)

db = utils.find_tables_for('Human')[0]
connection = utils.connect_to_db(db)
gene_tables = utils.get_table_names(connection)


data = utils.get_table(gene_tables[0], connection)
data = [utils.format_gene(variant) for variant in data]


names = [item['qName'] for item in data]

genes = {}

for name in names:
    genes[name] = []

for gene in data:
    genes[gene['qName']].append(gene)


with open('genes.json', 'w') as f:
    json.dump(genes, f, indent=4)

print(genes)