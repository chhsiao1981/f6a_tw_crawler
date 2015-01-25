# -*- coding: utf-8 -*-

import ujson as json
import pandas as pd
import numpy as np
import re
import argparse

from f6a_tw_crawler.constants import *
from f6a_tw_crawler import cfg
from f6a_tw_crawler import util
from f6a_tw_crawler import util_pd
from f6a_tw_crawler import util_lock

df_columns = ['the_id', 'name', 'provider', 'the_type', 'update_date', 'desc', 'columns', 'the_url']


def meta_json_to_csv(last_n):
    results = [_get_meta(idx) for idx in range(1, last_n)]

    results = [each_result for each_result in results if each_result]

    df = pd.DataFrame(results)

    for idx in df.columns:
        if df[idx].dtype == 'object':
            df[idx] = df[idx].apply(lambda x: _str_or_list(x))

    df = df[df_columns]

    df.to_csv('data/meta/meta.csv', index=False)


def _str_or_list(x):
    if x.__class__.__name__ == 'unicode':
        return x.encode('utf-8')
    elif x.__class__.__name__ == 'list':
        return json.dumps(x)
    else:
        return x


def _get_meta(idx):
    meta = {}
    filename = 'data/meta/' + str(idx) + '.meta.json'
    try:
        with open(filename, 'r') as f:
            meta = json.load(f)
        meta = meta[0]
    except Exception as e:
        cfg.logger.error('unable to load meta: idx: %s filename: %s e: %s', idx, filename, e)
        meta = {}
    meta['desc'] = meta['desc'].strip()

    return meta


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='f6a_tw_crawler')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-n', '--last_n', type=int, required=True, help="end numbers of data")

    args = parser.parse_args()

    return (S_OK, args)


def _main():
    (error_code, args) = parse_args()

    cfg.init({'ini_filename': args.ini})

    meta_json_to_csv(args.last_n)


if __name__ == '__main__':
    _main()
