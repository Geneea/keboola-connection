# coding=utf-8

from mainTools import main

def create_results(doc):
    yield {
        'topic': doc['topic'].encode('utf-8'),
        'confidence': str(doc['confidence'])
    }

def one_to_many():
    return False

def csv_header():
    return ['topic', 'confidence']

if __name__ == '__main__':
    main('topic', csv_header(), create_results, one_to_many())
