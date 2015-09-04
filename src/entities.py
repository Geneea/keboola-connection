# coding=utf-8

from mainTools import main

def create_results(doc):
    e = doc['entities']
    for i in xrange(len(e)):
        yield {
            'entity': e[i]['name'].encode('utf-8'),
            'type': e[i]['type'].encode('utf-8'),
            'textOffset': str(e[i]['textOffset']),
            'sentiment': str(e[i]['sentiment'])
        }

if __name__ == '__main__':
    main('entities', ['entity', 'type', 'textOffset', 'sentiment'], create_results)
