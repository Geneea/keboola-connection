# coding=utf-8

from mainTools import main

def create_results(doc):
    yield {
        'sentiment': str(doc['sentiment'])
    }

def one_to_many():
    return False

def csv_header():
    return ['sentiment']

if __name__ == '__main__':
    main('sentiment', csv_header(), create_results, one_to_many())
