# coding=utf-8

import csv

from mainTools import main, unfussy_csv_reader, slice_stream, make_request

def lemmatize(config):
    with open(config.input_path, 'rb') as input_file, open(config.output_path, 'wb') as output_file:
        reader = unfussy_csv_reader(input_file)

        writer = csv.DictWriter(output_file, fieldnames=[config.id_col, 'lemma', 'lemmaIndex'])
        writer.writeheader()

        for rows in slice_stream(reader, 100):
            results = make_request(config, 'lemmatize', rows)
            for doc in results:
                doc_id = doc['id'].encode('utf-8')
                lemmas = doc['lemmas']
                for i in xrange(len(lemmas)):
                    writer.writerow({
                        config.id_col: doc_id,
                        'lemma': lemmas[i].encode('utf-8'),
                        'lemmaIndex': str(i)
                    })

if __name__ == '__main__':
    main(lemmatize)
