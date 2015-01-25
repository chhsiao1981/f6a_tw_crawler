#!/bin/bash

if [ "${BASH_ARGC}" != "1" ]
then
  echo "usage: craw_all_meta.sh [n]"
  exit
fi

n="${BASH_ARGV[0]}"

mkdir -p data/meta

for ((j = 1; j <= ${n}; j++))
do
  echo "${j}"
  cd f6a_tw_scrapy
  scrapy crawl f6a_tw_list -a no=${j} -o - -t json > ../data/meta/${j}.meta.json
  cd ..
done
