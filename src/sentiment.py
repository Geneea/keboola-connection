# coding=utf-8

from mainTools import main

def create_results(doc):
    yield {
        'sentiment': str(doc['sentiment'])
    }

def csv_header():
    return ['sentiment']

if __name__ == '__main__':
    main('sentiment', csv_header(), create_results)
