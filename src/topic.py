# coding=utf-8

from mainTools import main

def create_results(doc):
    yield {
        'topic': doc['topic'].encode('utf-8'),
        'confidence': str(doc['confidence'])
    }

if __name__ == '__main__':
    main('topic', ['topic', 'confidence'], create_results)
