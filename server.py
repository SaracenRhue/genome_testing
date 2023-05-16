from flask import Flask, request, jsonify
import utils

app = Flask(__name__)

@app.route('/process-data', methods=['POST'])
def process_data():
    data = request.json['data']
    print('Received data:', data)

    
    connection = utils.connect_to_db('hgcentral')
    dbDb = utils.get_table('dbDb', connection)

    db = utils.find_tables_for(data)[0]
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

        processed_data = data

        # Send the processed data back as a response
        return jsonify({'data': processed_data})

if __name__ == '__main__':
    app.run(host='localhost', port=3000)
