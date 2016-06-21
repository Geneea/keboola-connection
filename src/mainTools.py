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
MAX_REQ_SIZE = 100 * 1024
DOC_BATCH_SIZE = 12
CONNECT_TIMEOUT = 10.01
READ_TIMEOUT = 128

DOC_COUNT = 0

try:
    from requests.packages import urllib3
    urllib3.disable_warnings()
except ImportError:
    pass

class Config:
    def __init__(self, data_dir, config):
        self.input_path = data_dir + '/in/tables/' + config['storage']['input']['tables'][0]['source']
        if 'output' in config['parameters']:
            self.output_path = data_dir + '/out/tables/' + config['parameters']['output']
        else:
            self.output_path = data_dir + '/out/tables/' + config['storage']['output']['tables'][0]['source']
        self.user_key = config['parameters']['user_key']
        self.id_col = config['parameters']['id_column']
        self.data_col = config['parameters']['data_column']
        self.language = config['parameters']['language'] if 'language' in config['parameters'] else None
        self.analysis_types = config['parameters']['analysis_types'] if 'analysis_types' in config['parameters'] else []
        self.domain = config['parameters']['domain'] if 'domain' in config['parameters'] else None
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

    url = (BASE_URL if not config.use_beta else BETA_URL) + api_method
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'user_key ' + config.user_key
    }
    data = {
        'customerId': config.customer_id,
        'language': config.language,
        'domain': config.domain,
        'documents': documents
    }
    if len(config.analysis_types) > 0:
        data['analysisTypes'] = map(lambda t: str(t).lower(), config.analysis_types)

    response = json_post(url, headers, data)
    if len(response) > 0:
        global DOC_COUNT
        DOC_COUNT += len(documents)
        print >> sys.stdout, "successfully processed {n} documents".format(n=DOC_COUNT)
        sys.stdout.flush()
    else:
        ids = ','.join(map(lambda doc: doc['id'], documents))
        print >> sys.stdout, "failed to process documents {ids}".format(ids=ids)
        sys.stdout.flush()
        sys.stderr.flush()

    return response

def json_post(url, headers, data):
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
        if response.status_code >= 400:
            try:
                err = response.json()
                print >> sys.stderr, "HTTP error {code}, {e}: {msg}".format(
                    code=response.status_code, e=err['exception'], msg=err['message']
                )
            except ValueError:
                err = response.text
                print >> sys.stderr, "HTTP error {code}\n{e}".format(code=response.status_code, e=err)

            return []
    except requests.RequestException as e:
        print >> sys.stderr, "HTTP request exception\n{type}: {e}".format(type=type(e).__name__, e=e)
        return []

    return response.json()

def main(analysis_type, csv_header, create_results_fn):
    try:
        config = parse_config()

        with open(config.input_path, 'rb') as input_file, open(config.output_path, 'wb') as output_file:
            reader = unfussy_csv_reader(input_file)

            csv_header = [config.id_col] + csv_header
            writer = csv.DictWriter(output_file, fieldnames=csv_header)
            writer.writeheader()

            for rows in slice_stream(reader, DOC_BATCH_SIZE):
                for doc in make_request(config, analysis_type, rows):
                    for res_row in create_results_fn(doc):
                        res_row[config.id_col] = doc['id'].encode('utf-8')
                        writer.writerow(res_row)

        print >> sys.stdout, "the analysis finished"
        sys.exit(0)
    except (LookupError, IOError) as e:
        print >> sys.stderr, "{type}: {e}".format(type=type(e).__name__, e=e)
        sys.exit(1)
    except Exception as e:
        print >> sys.stderr, "{type}: {e}".format(type=type(e).__name__, e=e)
        sys.exit(2)
