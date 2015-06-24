# coding=utf-8

import csv

from mainTools import main, unfussy_csv_reader, slice_stream, make_request

def correction(config):
    with open(config.input_path, 'rb') as input_file, open(config.output_path, 'wb') as output_file:
        reader = unfussy_csv_reader(csv.DictReader(input_file))

        writer = csv.DictWriter(output_file, fieldnames=[config.id_col, 'correctedText', 'isCorrected', 'isDiacritized'])
        writer.writeheader()

        for rows in slice_stream(reader, 100):
            results = make_request(config, 'correction', rows)
            for doc in results:
                writer.writerow({
                    config.id_col: doc['id'].encode('utf-8'),
                    'correctedText': doc['correctedText'].encode('utf-8'),
                    'isCorrected': str(doc['corrected']),
                    'isDiacritized': str(doc['diacritized'])
                })

if __name__ == '__main__':
    main(correction)
