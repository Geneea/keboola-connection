# coding=utf-8

from mainTools import main

def create_results(doc):
    lemmas = doc['lemmas']
    for i in xrange(len(lemmas)):
        yield {
            'lemma': lemmas[i].encode('utf-8'),
            'lemmaIndex': str(i)
        }

if __name__ == '__main__':
    main('lemmatize', ['lemma', 'lemmaIndex'], create_results)
