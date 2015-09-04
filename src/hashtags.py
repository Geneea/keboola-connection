# coding=utf-8

from mainTools import main

def create_results(doc):
    hashtags = doc['hashtags']
    for i in xrange(len(hashtags)):
        yield {
            'hashtag': hashtags[i]['text'].encode('utf-8'),
            'score': str(hashtags[i]['score'])
        }

if __name__ == '__main__':
    main('hashtags', ['hashtag', 'score'], create_results)
