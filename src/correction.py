# coding=utf-8

import csv

from mainTools import main, make_request

def correction(config):
    with open(config.input_path, 'rb') as input_file, open(config.output_path, 'wb') as output_file:
        reader = csv.DictReader(input_file)
        rows = list(reader)

        results = make_request(config, 'correction', rows)

        writer = csv.DictWriter(output_file, fieldnames=[config.id_col, 'correctedText', 'isCorrected', 'isDiacritized'])
        writer.writeheader()

        for doc in results:
            writer.writerow({
                config.id_col: doc['id'].encode('utf-8'),
                'correctedText': doc['correctedText'].encode('utf-8'),
                'isCorrected': doc['corrected'].encode('utf-8'),
                'isDiacritized': doc['diacritized'].encode('utf-8')
            })

if __name__ == '__main__':
    main(correction)
