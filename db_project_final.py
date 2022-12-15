## RsNBEFoIkVgHFTC5vySKRIXFzzGeNvyOy01nxidgIcmd4nWkNhx7KjLGut0ylC9HJoWcssXybeuaxW%2BArMI7Yg%3D%3D

import requests, bs4
import pandas as pd
from lxml import html
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from tabulate import tabulate

def build_youtube_search(developer_key):
  DEVELOPER_KEY = developer_key
  YOUTUBE_API_SERVICE_NAME="youtube"
  YOUTUBE_API_VERSION="v3"
  return build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

def get_search_response(youtube, query):
  search_response = youtube.search().list(
    q = query,
    order = "relevance",
    part = "snippet",
    maxResults = 10
    ).execute()
  return search_response

def get_video_info(search_response):
  result_json = {}
  idx =0
  for item in search_response['items']:
    if item['id']['kind'] == 'youtube#video':
      result_json[idx] = info_to_dict(item['id']['videoId'], item['snippet']['title'], item['snippet']['description'], item['snippet']['thumbnails']['medium']['url'])
      idx += 1
  return result_json

def info_to_dict(videoId, title, description, url):
  result = {
      "videoId": videoId,
      "title": title,
      "description": description,
      "url": url
  }
  return result

xmlUrl = 'http://openapi.1365.go.kr/openapi/service/rest/VolunteerPartcptnService/getVltrSearchWordList'
My_API_Key = unquote('RsNBEFoIkVgHFTC5vySKRIXFzzGeNvyOy01nxidgIcmd4nWkNhx7KjLGut0ylC9HJoWcssXybeuaxW%2BArMI7Yg%3D%3D')

API_youtube_KEY = 'AIzaSyDWWdkw0CzZdVZs6k6zMK-sW5hFoBcxaaM'

K = 'keyword=' + input("키워드를 입력하시오: ")
P = 'actPlace=' + input("지역을 입력하시오: ")

response = requests.get(xmlUrl + '?' + K + '&' + P).text.encode('utf-8')
xmlobj = bs4.BeautifulSoup(response, 'lxml-xml')

# print(xmlUrl+queryParams)

rows = xmlobj.findAll('item')
#columns = rows[0].find_all()

rowList = []
nameList = []
columnList = []

rowsLen = len(rows)
for i in range(0, rowsLen):
    columns = rows[i].find_all()
    
    columnsLen = len(columns)
    for j in range(0, columnsLen):
        if columns[j].name != 'actBeginTm' and columns[j].name != 'actEndTm' and columns[j].name != 'actPlace' and columns[j].name != 'nanmmbyNm' and columns[j].name != 'noticeBgnde' and columns[j].name != 'noticeEndde' and columns[j].name != 'progrmBgnde' and columns[j].name != 'progrmEndde' and columns[j].name != 'progrmSi' and columns[j].name != 'progrmSttusSe':
            continue
        if i == 0:
            nameList.append(columns[j].name)
        eachColumn = columns[j].text
        columnList.append(eachColumn)
    rowList.append(columnList)
    columnList = []

nameList[0] = '시작 시간'
nameList[1] = '종료 시간'
nameList[2] = '장소'
nameList[3] = '지역(시설)'
nameList[4] = '모집 시작 날짜'
nameList[5] = '모집 끝 날짜'
nameList[6] = '프로그램 시작 날짜'
nameList[7] = '프로그램 끝 날짜'
nameList[8] = '모집 상태'

for i in range(len(rowList)):
  if(rowList[i][8]) == '1':
    rowList[i][8] = '모집 대기'
  elif(rowList[i][8]) == '2':
    rowList[i][8] = '모집중'
  elif(rowList[i][8]) == '3':
    rowList[i][8] = '모집 완료'

result = pd.DataFrame(rowList, columns=nameList)
print(tabulate(result.head(5), headers='keys', tablefmt='fancy_grid', showindex=True, numalign='center'))

#print(result.head(10))
#print(result['actBeginTm'])
#print(result)

youtube = build_youtube_search(API_youtube_KEY)
search_response = get_search_response(youtube, K + '봉사 팁')
result_json = get_video_info(search_response)

for i in range(3):
    seq = result_json[i]
    print(seq['title'], 'https://www.youtube.com/watch?v=' + seq['videoId'])