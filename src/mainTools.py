# coding=utf-8

import argparse
import csv
import itertools
import json
import os
import sys

import requests
import yaml

BASE_URL = 'https://api.geneea.com/keboola/'
BETA_URL = 'https://beta-api.geneea.com/keboola/'
MAX_REQ_SIZE = 400 * 1024
DOC_COUNT = 0

try:
    from requests.packages import urllib3
    urllib3.disable_warnings()
except ImportError:
    pass

class Config:
    def __init__(self, data_dir, config):
        self.input_path = data_dir + '/in/tables/' + config['storage']['input']['tables'][0]['source']
        self.output_path = data_dir + '/out/tables/' + config['storage']['output']['tables'][0]['source']
        self.user_key = config['parameters']['user_key']
        self.id_col = config['parameters']['id_column']
        self.data_col = config['parameters']['data_column']
        self.language = config['parameters']['language'] if 'language' in config['parameters'] else None
        self.use_beta = config['parameters']['use_beta'] if 'use_beta' in config['parameters'] else False

        self.customer_id = os.environ['KBC_PROJECTID']

def parse_config():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-d', '--data', dest='data_dir', required=True)
    args = argparser.parse_args()

    with open(args.data_dir + '/config.yml', 'r') as config_file:
        config = yaml.load(config_file)
        return Config(args.data_dir, config)

def unfussy_csv_reader(input_file):
    safe_input = itertools.imap(lambda line: line.replace('\0', ''), input_file)
    csv_reader = csv.DictReader(safe_input)
    while True:
        try:
            yield next(csv_reader)
        except csv.Error as e:
            print >> sys.stderr, "CSV read error: {e}".format(e=e)
            raise StopIteration

def slice_stream(iterator, size):
    while True:
        chunk = list(itertools.islice(iterator, size))
        if not chunk:
            raise StopIteration
        else:
            yield chunk

def make_request(config, api_method, rows):
    size = itertools.imap(lambda row: len(row[config.data_col]), rows)
    size = reduce(lambda x, y: x + y, size)
    if size > MAX_REQ_SIZE:
        if len(rows) == 1:
            print >> sys.stderr, "document {id} is too large".format(id=rows[0][config.id_col])
            sys.stderr.flush()
            return []

        half = len(rows) / 2
        return itertools.chain(
            make_request(config, api_method, rows[:half]),
            make_request(config, api_method, rows[half:])
        )

    documents = map(lambda row: {'id': row[config.id_col], 'text': row[config.data_col]}, rows)
    documents = filter(lambda doc: len(doc['text']) > 0, documents)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'user_key ' + config.user_key
    }
    data = {
        'customerId': config.customer_id,
        'language': config.language,
        'documents': documents
    }

    url = (BASE_URL if not config.use_beta else BETA_URL) + api_method
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code >= 400:
        ids = ','.join(map(lambda doc: doc['id'], documents))
        try:
            err = response.json()
            print >> sys.stderr, "HTTP error {code}, {e}: {msg} (for documents {ids})".format(
                code=response.status_code, e=err.exception, msg=err.message, ids=ids
            )
        except ValueError:
            err = response.text()
            print >> sys.stderr, "HTTP error {code} (for documents {ids})\n{e}".format(
                code=response.status_code, ids=ids, e=err
            )
        sys.stderr.flush()

        return []

    global DOC_COUNT
    DOC_COUNT += len(documents)
    print >> sys.stdout, "successfully processed {n} documents".format(n=DOC_COUNT)
    sys.stdout.flush()

    return response.json()

def main(function):
    try:
        config = parse_config()
        function(config)
        print >> sys.stdout, "the analysis finished"
        sys.exit(0)
    except (LookupError, IOError) as e:
        print >> sys.stderr, "{type}: {e}".format(type=type(e).__name__, e=e)
        sys.exit(1)
    except Exception as e:
        print >> sys.stderr, "{type}: {e}".format(type=type(e).__name__, e=e)
        sys.exit(2)
