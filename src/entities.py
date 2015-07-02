# coding=utf-8

import csv

from mainTools import main, unfussy_csv_reader, slice_stream, make_request

def entities(config):
    with open(config.input_path, 'rb') as input_file, open(config.output_path, 'wb') as output_file:
        reader = unfussy_csv_reader(input_file)

        writer = csv.DictWriter(output_file, fieldnames=[config.id_col, 'entity', 'type', 'textOffset', 'sentiment'])
        writer.writeheader()

        for rows in slice_stream(reader, 100):
            results = make_request(config, 'entities', rows)
            for doc in results:
                doc_id = doc['id'].encode('utf-8')
                e = doc['entities']
                for i in xrange(len(e)):
                    writer.writerow({
                        config.id_col: doc_id,
                        'entity': e[i]['name'].encode('utf-8'),
                        'type': e[i]['type'].encode('utf-8'),
                        'textOffset': str(e[i]['textOffset']),
                        'sentiment': str(e[i]['sentiment'])
                    })

if __name__ == '__main__':
    main(entities)
