# coding=utf-8

from mainTools import main

def create_results(doc):
    yield {
        'correctedText': doc['correctedText'].encode('utf-8'),
        'isCorrected': str(doc['corrected']),
        'isDiacritized': str(doc['diacritized'])
    }

if __name__ == '__main__':
    main('correction', ['correctedText', 'isCorrected', 'isDiacritized'], create_results)
