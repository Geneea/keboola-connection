# coding=utf-8

import csv

from mainTools import main, unfussy_csv_reader, slice_stream, make_request

def sentiment(config):
    with open(config.input_path, 'rb') as input_file, open(config.output_path, 'wb') as output_file:
        reader = unfussy_csv_reader(input_file)

        writer = csv.DictWriter(output_file, fieldnames=[config.id_col, 'sentiment'])
        writer.writeheader()

        for rows in slice_stream(reader, 100):
            results = make_request(config, 'sentiment', rows)
            for doc in results:
                writer.writerow({
                    config.id_col: doc['id'].encode('utf-8'),
                    'sentiment': str(doc['sentiment'])
                })

if __name__ == '__main__':
    main(sentiment)
