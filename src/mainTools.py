# coding=utf-8

import sys
import argparse
import json
import csv

import requests
import yaml

BASE_URL = 'https://api.geneea.com/keboola/'

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
        self.customer_id = config['parameters']['customer_id']
        self.id_col = config['parameters']['id_column']
        self.data_col = config['parameters']['data_column']
        self.language = config['parameters']['language'] if 'language' in config['parameters'] else None

def parse_config():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-d', '--data', dest='data_dir', required=True)
    args = argparser.parse_args()

    with open(args.dataDir + '/config.yml', 'r') as config_file:
        config = yaml.load(config_file)
        return Config(args.data_dir, config)

def make_request(config, api_method, rows):
    documents = map(lambda row: {'id': row[config.id_col], 'text': row[config.data_col]}, rows)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'user_key ' + config.user_key
    }
    data = {
        'customerId': config.customer_id,
        'language': config.language,
        'documents': documents
    }

    print >> sys.stdout, "sending {n} documents for analysis".format(n=len(documents))
    sys.stdout.flush()

    response = requests.post(BASE_URL + api_method, headers=headers, data=json.dumps(data))
    response.raise_for_status()

    return response.json()

def main(function):
    try:
        config = parse_config()
        function(config)
        print >> sys.stdout, "successfully finished"
        sys.exit(0)
    except (LookupError, IOError, csv.Error) as e:
        print >> sys.stderr, "{type}: {e}".format(type=type(e).__name__, e=e)
        sys.exit(1)
    except Exception as e:
        print >> sys.stderr, "{type}: {e}".format(type=type(e).__name__, e=e)
        sys.exit(2)
