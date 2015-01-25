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


def json_to_csv(filename):
    with open(filename, 'r') as f:
        the_struct = json.load(f)

    the_struct = [_parse_struct(each_struct) for each_struct in the_struct]

    filename_meta = re.sub(ur'json$', 'meta.json', re.sub('^data', 'data/meta', filename))

    columns = []

    with open(filename_meta, 'r') as f:
        struct_meta = json.load(f)
        if struct_meta:
            columns = struct_meta[0].get('columns', [])
            columns = [each_column.encode('utf-8') for each_column in columns]

    df = pd.DataFrame(the_struct)

    if columns:
        df = df[columns]

    out_filename = re.sub(ur'.json$', '.csv', filename)

    cfg.logger.debug('to csv: out_filename: %s', out_filename)
    df.to_csv(out_filename, index=False)


def _parse_struct(dict_list):
    result = {}

    for each_dict in dict_list:
        result.update(each_dict)

    result = {key.encode('utf-8'): re.sub(ur'\n', ' ', val).encode('utf-8') for (key, val) in result.iteritems()}

    return result


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='f6a_tw_crawler')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-f', '--filename', type=str, required=True, help="filename")

    args = parser.parse_args()

    return (S_OK, args)


def _main():
    (error_code, args) = parse_args()

    cfg.init({'ini_filename': args.ini})

    json_to_csv(args.filename)


if __name__ == '__main__':
    _main()
