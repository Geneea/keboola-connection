# coding=utf-8

import csv

from mainTools import main, make_request

def sentiment(config):
    with open(config.input_path, 'rb') as input_file, open(config.output_path, 'wb') as output_file:
        reader = csv.DictReader(input_file)
        rows = list(reader)

        results = make_request(config, 'sentiment', rows)

        writer = csv.DictWriter(output_file, fieldnames=[config.id_col, 'sentiment'])
        writer.writeheader()

        for doc in results:
            writer.writerow({
                config.id_col: doc['id'].encode('utf-8'),
                'sentiment': str(doc['sentiment'])
            })

if __name__ == '__main__':
    main(sentiment)
