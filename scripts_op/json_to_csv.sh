#!/bin/bash

if [ "${BASH_ARGC}" != "1" ]
then
  echo "usage: json_to_csv.sh [filename]"
  exit
fi

filename="${BASH_ARGV[0]}"

echo "filename: ${filename}"
python -m f6a_tw_crawler.json_to_csv -i development.ini -f ${filename}
