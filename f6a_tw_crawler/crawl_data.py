# -*- coding: utf-8 -*-

# import ujson as json
import pandas as pd
import numpy as np
import re
import argparse
import simplejson as json
from StringIO import StringIO
import logging

from f6a_tw_crawler.constants import *
from f6a_tw_crawler import cfg
from f6a_tw_crawler import util
from f6a_tw_crawler import util_pd
from f6a_tw_crawler import util_lock


def crawl_data(no):
    url_csv = 'http://data.fda.gov.tw/cacheData/' + str(no) + '_2.csv'
    url_json = 'http://data.fda.gov.tw/cacheData/' + str(no) + '_3.json'

    filename_csv = 'data/' + str(no) + '.csv'
    filename_json = 'data/' + str(no) + '.json'
    filename_meta = 'data/meta/' + str(no) + '.meta.json'
    util.makedirs('data')

    contents = util.http_multiget([url_csv, url_json])

    content_json = contents.get(url_json, '')
    content_csv = contents.get(url_csv, '')
    content_csv = re.sub(ur'\t+\r?\n', '\n', content_csv, re.M)

    columns = []
    try:
        with open(filename_meta, 'r') as f:
            content_meta = json.load(f)
            if content_meta:
                columns = content_meta[0].get('columns', [])
            columns = [each_column.encode('utf-8') for each_column in columns]

            # columns.append('')
    except Exception as e:
        logging.error('unable to get meta data: e: %s', e)
        columns = []

    if not columns:
        columns = None

    '''
    if content_json:
        with open(filename_json + '.raw', 'w') as f:
            f.write(content_json)
    '''

    if content_csv:
        with open(filename_csv + '.raw', 'w') as f:
            f.write(content_csv)

    if content_json:
        content_json = content_json.decode('utf-8')
        the_struct_json = []
        try:
            the_struct_json = json.loads(content_json)
        except Exception as e:
            cfg.logger.error('unable to json.loads: e: %s', e)
            the_struct_json = []

        with open(filename_json, 'w') as f:
            json.dump(the_struct_json, f, indent=2)

    cfg.logger.debug('columns: %s', columns)

    if content_csv:
        content_csv = content_csv.decode('utf-8')
        content_csv = content_csv[1:]
        content_csv = content_csv.encode('utf-8')
        f = StringIO(content_csv)
        df = pd.read_csv(f, sep='\t', names=columns, header=None, skipinitialspace=True)
        df.to_csv(filename_csv, index=False)


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='f6a_tw_crawler')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-n', '--no', type=str, required=True, help="id-number of the data")

    args = parser.parse_args()

    return (S_OK, args)


def _main():
    (error_code, args) = parse_args()

    cfg.init({'ini_filename': args.ini, 'no': args.no})

    crawl_data(args.no)


if __name__ == '__main__':
    _main()
