# coding=utf-8

from mainTools import main

def create_results(doc):
    lemmas = doc['lemmas']
    for i in xrange(len(lemmas)):
        yield {
            'lemma': lemmas[i].encode('utf-8'),
            'lemmaIndex': str(i)
        }

def one_to_many():
    return True

def csv_header():
    return ['lemma', 'lemmaIndex']

if __name__ == '__main__':
    main('lemmatize', csv_header(), create_results, one_to_many())
