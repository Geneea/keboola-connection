# coding=utf-8

from mainTools import main

def create_results(doc):
    yield {
        'sentiment': str(doc['sentiment'])
    }

if __name__ == '__main__':
    main('sentiment', ['sentiment'], create_results)
