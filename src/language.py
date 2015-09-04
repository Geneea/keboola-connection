# coding=utf-8

from mainTools import main

def create_results(doc):
    yield {
        'language': doc['language'].encode('utf-8')
    }

def csv_header():
    return ['language']

if __name__ == '__main__':
    main('language', csv_header(), create_results)
