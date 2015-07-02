# coding=utf-8

import csv

from mainTools import main, unfussy_csv_reader, slice_stream, make_request

def topic(config):
    with open(config.input_path, 'rb') as input_file, open(config.output_path, 'wb') as output_file:
        reader = unfussy_csv_reader(input_file)

        writer = csv.DictWriter(output_file, fieldnames=[config.id_col, 'topic', 'confidence'])
        writer.writeheader()

        for rows in slice_stream(reader, 100):
            results = make_request(config, 'topic', rows)
            for doc in results:
                writer.writerow({
                    config.id_col: doc['id'].encode('utf-8'),
                    'topic': doc['topic'].encode('utf-8'),
                    'confidence': str(doc['confidence'])
                })

if __name__ == '__main__':
    main(topic)
