import utils
import json
from pick import pick

data = {}
connection = utils.connect_to_db('hgcentral')
dbDb = utils.get_table('dbDb', connection)

options = [item['organism'] for item in dbDb]



title = 'Select genomes (press SPACE to mark, ENTER to continue): '
selected = pick(options, title, multiselect=True, min_selection_count=1)

for item in selected:

    name =  item[0]
    try:
        db = utils.find_table_for(name)
        connection = utils.connect_to_db(db)
        organism_tables = utils.get_table_names(connection)
        organism = utils.get_table(organism_tables[0], connection)
    except: 
        print(f'Could not find {name}')
        continue
    for variant in organism:
        var_keys = list(variant.keys())
        for key in var_keys:
            variant[key] = str(variant[key]).replace("b'", '').replace(",'", '')
            if ',' in variant[key]:
                variant[key] = variant[key].split(',')
            try:
                if type(variant[key]) == list:
                    for i in range(len(variant[key])):
                        variant[key][i] = int(variant[key][i])
                else:
                    variant[key] = int(variant[key])
            except: ValueError 
            pass
    print(name)
    name = str(name).replace(' ', '_').lower()
    data[name] = organism

with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)