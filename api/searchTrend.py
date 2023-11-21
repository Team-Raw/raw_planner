import os
import sys
import urllib.request
from define import const
import json

def search_data():
    client_id = const.SEARCH_API_CLIENT_ID
    client_secret = const.SEARCH_API_CLIENT_SECRET
    search_data = make_temp_data()
    print(search_data)
    url = const.SEARCH_API_BASE_URL
    body = json.dumps(search_data)

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        print('')
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)


def make_temp_data():
    return {
        'startDate' : '2017-01-01',
        'endDate' : '2023-01-01',
        'timeUnit' : 'month',
        # 'keywordGroups' : [{"groupName":"한글","keywords":["한글","korean"]},{"groupName":"영어","keywords":["영어","english"]}],
        'keywordGroups' : [{"groupName":"자동차","keywords":["현대","기아"]}],
        'device' : 'pc',
        'ages' : ["1","2"],
        'gender' : 'f'
    }