import os
import json
import utils


genomes =[]

for file in os.listdir('./genome_files'):
# extract the data from the file
    with open(f'./genome_files/{file}', 'r') as f:
        data = f.read()
        #create 2d array of the data with each row being a array
        data = [i.split() for i in data.split('\n')]
        

        for line in data:
            if line == []:
                data.remove(line)
        # remove additional column if it exists
        if data[0][0] == '#bin':
            for line in data:
                    line.pop(0)
        data.pop(0)
    

    genome = {'variants': []}
    for i in range(len(data)):
        exon_starts = data[i][8][:-1]
        
        exon_ends = data[i][9][:-1]
        exon_starts = [int(i) for i in exon_starts.split(',')]
        exon_ends = [int(i) for i in exon_ends.split(',')]
        econ_count = data[i][7]
        sequence = utils.generate_sequence(exon_starts, exon_ends)
        genome['variants'].append({
                'name': data[i][0],
                'genome_start': exon_starts[0],
                'genome_end': exon_ends[-1],
                'genome_length': exon_ends[-1] - exon_starts[0],
                'econ_count': econ_count,
                'exon_starts': exon_starts,
                'exon_ends': exon_ends,
                'sequence': sequence
            })


    genomes.append(genome)


with open('genomes.json', 'w') as f:
    json.dump(genomes, f, indent=4)