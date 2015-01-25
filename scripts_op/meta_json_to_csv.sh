#!/bin/bash

if [ "${BASH_ARGC}" != "1" ]
then
  echo "usage: meta_json_to_csv.sh [n]"
  exit
fi

n="${BASH_ARGV[0]}"

python -m f6a_tw_crawler.meta_json_to_csv -i development.ini -n ${n}
