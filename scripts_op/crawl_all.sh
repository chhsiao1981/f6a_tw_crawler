#!/bin/bash

if [ "${BASH_ARGC}" != "1" ]
then
  echo "usage: craw_all.sh [n]"
  exit
fi

n="${BASH_ARGV[0]}"

for ((j = 1; j <= ${n}; j++))
do
  is_skip=false
  #  6: unknown
  # 26: unknown
  # 27: unknown
  # 33: 2014 年 9 月餿水油受影響廠商 (過期)
  # 69: 醫療器材相關資訊 (似乎是過期? 因為 68 也有類似資訊?)
  # 92: unknown
  # 93: unknown
  for k in 6 26 27 33 69 92 93
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
  sleep 1
done
