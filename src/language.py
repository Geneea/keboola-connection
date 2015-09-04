# coding=utf-8

from mainTools import main

def create_results(doc):
    yield {
        'language': doc['language'].encode('utf-8')
    }

if __name__ == '__main__':
    main('language', ['language'], create_results)
