# coding=utf-8

from mainTools import main

def create_results(doc):
    hashtags = doc['hashtags']
    for i in xrange(len(hashtags)):
        yield {
            'hashtag': hashtags[i]['text'].encode('utf-8'),
            'score': str(hashtags[i]['score'])
        }

def csv_header():
    return ['hashtag', 'score']

if __name__ == '__main__':
    main('hashtags', csv_header(), create_results)
