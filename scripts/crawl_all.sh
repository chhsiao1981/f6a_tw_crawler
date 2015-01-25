#!/bin/bash

for ((j = 1; j <= 119; j++))
do
  is_skip=false
  # 26: unknown
  # 27: unknown
  # 33: 2014 年餿水油受影響廠商 (過期)
  # 69: 醫療器材
  # 92: unknown
  # 93: unknown
  for k in 26 27 33 69 92 93
  do
    if [ "${j}" == "${k}" ]
    then
      echo "to skip: ${j}"
      is_skip="true"
    fi
  done
  if [ "${is_skip}" == "true" ]
  then
    continue
  fi

  echo "${j}"
  python -m f6a_tw_crawler.crawl_data -i development.ini -n ${j}
done
