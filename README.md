f6a_tw_crawler
================

Introduction
-----
這是 Python 版本的對於 http://data.fda.gov.tw 的 data crawler.

其他相關的 link:
* 官方網站: http://data.fda.gov.tw
* php 版本: https://github.com/kiang/data.fda.gov.tw

Install
-----
virtualenv __; . __/bin/activate; pip install -r requirements.txt

Usage
-----
* meta: ./scripts_op/crawl_all_meta.sh [n]
* meta_json_to_csv: ./scripts_op/meta_json_to_csv.sh [n]
* data: ./scripts_op/crawl_all.sh [n]
* json_to_csv: ./scripts_op/json_to_csv.sh [json_filename] (good for broken csv files)

Meta:
-----
https://docs.google.com/spreadsheets/d/1T4orerlQuaKZ8dGLJCJi02EgpFS2gTjSQMMsl7vB-HI/edit#gid=0
