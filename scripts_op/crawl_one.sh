#!/bin/bash

if [ "${BASH_ARGC}" != "1" ]
then
  echo "usage: crawl_one.sh [n]"
  exit
fi

j="${BASH_ARGV[0]}"

is_skip=false
#  6: 廚師證書資料集
# 26: unknown
# 27: unknown
# 33: 2014 年 9 月餿水油受影響廠商 (過期)
# 69: 醫療器材詳細處方成分資料集
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
  exit
fi

echo "${j}"
echo "curl -s -i 'http://data.fda.gov.tw/opendata/exportDataList.do?method=ExportData&InfoId=${j}&logType=2'"
echo "curl -s -i 'http://data.fda.gov.tw/opendata/exportDataList.do?method=ExportData&InfoId=${j}&logType=3'"
curl_context=`curl -s -i "http://data.fda.gov.tw/opendata/exportDataList.do?method=ExportData&InfoId=${j}&logType=2"`
echo "curl_context: ${curl_context}"
zip_content=`echo "${curl_context}"|grep zip`
echo "zip_content: ${zip_content}"
  
if [ "${zip_content}" != "" ]
then
  python -m f6a_tw_crawler.crawl_data -i development.ini -n ${j} -z 1
else
  python -m f6a_tw_crawler.crawl_data -i development.ini -n ${j}
fi
