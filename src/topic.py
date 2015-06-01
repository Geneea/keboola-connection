# coding=utf-8

import csv

from mainTools import main, make_request

def topic(config):
    with open(config.input_path, 'rb') as input_file, open(config.output_path, 'wb') as output_file:
        reader = csv.DictReader(input_file)
        rows = list(reader)

        results = make_request(config, 'topic', rows)

        writer = csv.DictWriter(output_file, fieldnames=[config.id_col, 'topic', 'confidence'])
        writer.writeheader()

        for doc in results:
            writer.writerow({
                config.id_col: doc['id'].encode('utf-8'),
                'topic': doc['topic'].encode('utf-8'),
                'confidence': str(doc['confidence'])
            })

if __name__ == '__main__':
    main(topic)
