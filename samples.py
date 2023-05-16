import json
import utils

with open('samples.json', 'r') as f:
    data = json.load(f)

new_data = []
data_keys = list(data.keys())

for key in data_keys:
    data[key] = {
        'name': key,
        'variants': data[key], 
       # 'matrix': []
    }
    new_data.append(data[key])

    
# for gene in new_data:
#     gene['matrix'] = utils.create_matrix(gene['variants'])






with open('new.json', 'w') as f:
    json.dump(new_data, f)