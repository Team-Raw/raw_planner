import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

import urllib.request
import base64
import json
import warnings
from io import BytesIO

warnings.filterwarnings(action='ignore')

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.grid'] = False

pd.set_option('display.max_columns', 250)
pd.set_option('display.max_rows', 250)
pd.set_option('display.width', 100)

pd.options.display.float_format = '{:.2f}'.format

class NaverDataLabOpenAPI():
    """
    네이버 데이터랩 오픈 API 컨트롤러 클래스
    """

    def __init__(self, client_id, client_secret):
        """
        인증키 설정 및 검색어 그룹 초기화
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.keywordGroups = []
        self.url = "https://openapi.naver.com/v1/datalab/search"
        plt.rc('font', family='NanumGothic')

    def request_api(self, body):
        request = urllib.request.Request(self.url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        request.add_header("Content-Type","application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            return json.loads(response_body)
        else:
            print("Error Code:" + rescode)

    def add_keyword_groups(self, group_dict):
        """
        검색어 그룹 추가
        """

        keyword_gorup = {
            'groupName': group_dict['groupName'],
            'keywords': group_dict['keywords']
        }
        
        self.keywordGroups.append(keyword_gorup)
        print(f">>> Num of keywordGroups: {len(self.keywordGroups)}")

    # 연령별 그래프
    def get_result_age(self, startDate, endDate, timeUnit, device, ages, gender):

        age_conv={'1':'0∼12세','2':'13∼18세','3':'19∼24세','4':'25∼29세','5':'30∼34세',
            '6':'35∼39세','7':'40∼44세','8':'45∼49세','9':'50∼54세','10':'55∼59세','11':'60세 이상'}
        
        response_results_all = pd.DataFrame()
        
        for age in ages:
            body_dict={} #검색 정보를 저장할 변수
            body_dict['startDate']=startDate
            body_dict['endDate']=endDate
            body_dict['timeUnit']=timeUnit
            body_dict['keywordGroups']=self.keywordGroups
            body_dict['device']=device
            body_dict['gender']=gender
            body_dict['ages']=[age]

            body=str(body_dict).replace("'",'"') # ' 문자로는 에러가 발생해서 " 로 변환

            response_json = self.request_api(body)

            # 결과데이터중 'data' 와 'title'만 따로 DataFrame으로 저장
            response_results = pd.DataFrame()
            for data in response_json['results']:
                result=pd.DataFrame(data['data'])
                result['title']=data['title']
                result['age']=age # 연령대 정보를 추가

                response_results = pd.concat([response_results,result])
            
            response_results_all = pd.concat([response_results_all,response_results])
            
        #title별로 그래프를 그리기 위한부분
        titles=response_results['title'].unique() 

        graph_data = {}
        for age in ages:
            buf = BytesIO()
            plt.figure(figsize=(4,4))
            for title in titles:
                data=response_results_all.loc[(response_results_all['title']==title) 
                            & (response_results_all['age']==age),:]
                plt.plot(data['period'],data['ratio'],label=title)
                plt.xticks(rotation=90)
                plt.ylabel("검색량")
                plt.legend()
            plt.title(str(age_conv[age]))
            plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.3)  # 잘 맞게 조절
            plt.savefig(buf, format="png")
            graph_data[age] = base64.b64encode(buf.getbuffer()).decode("ascii")
        
        return graph_data
    
    # 기기별 그래프
    def get_result_device(self, startDate, endDate, timeUnit, device, ages, gender):
        devices = ['pc', 'mo']
        
        response_results_all = pd.DataFrame()
        
        for device in devices:
            body_dict={} #검색 정보를 저장할 변수
            body_dict['startDate']=startDate
            body_dict['endDate']=endDate
            body_dict['timeUnit']=timeUnit
            body_dict['keywordGroups']=self.keywordGroups
            body_dict['device']=device
            body_dict['gender']=gender
            body_dict['ages']=ages

            body=str(body_dict).replace("'",'"') # ' 문자로는 에러가 발생해서 " 로 변환

            response_json = self.request_api(body)

            # 결과데이터중 'data' 와 'title'만 따로 DataFrame으로 저장
            response_results = pd.DataFrame()
            for data in response_json['results']:
                result=pd.DataFrame(data['data'])
                result['title']=data['title']
                result['device']=device # 기기 정보를 추가

                response_results = pd.concat([response_results,result])
            
            response_results_all = pd.concat([response_results_all,response_results])
            
        #title별로 그래프를 그리기 위한부분
        titles=response_results['title'].unique() 

        graph_data = {}
        for device in devices:
            buf = BytesIO()
            plt.figure(figsize=(4,4))
            for title in titles:
                data=response_results_all.loc[(response_results_all['title']==title) 
                            & (response_results_all['device']==device),:]
                plt.plot(data['period'],data['ratio'],label=title)
                plt.xticks(rotation=90)
                plt.ylabel("검색량")
                plt.legend()
            if str(device) == 'pc':
                plt.title('PC')
            elif str(device) == 'mo':
                plt.title('MOBILE')
            plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.3)  # 잘 맞게 조절
            plt.savefig(buf, format="png")
            graph_data[device] = base64.b64encode(buf.getbuffer()).decode("ascii")
        
        return graph_data
    
    # 성별(남녀) 그래프
    def get_result_gender(self, startDate, endDate, timeUnit, device, ages, gender):
        genders = ['m', 'f']
        
        response_results_all = pd.DataFrame()
        
        for gender in genders:
            body_dict={} #검색 정보를 저장할 변수
            body_dict['startDate']=startDate
            body_dict['endDate']=endDate
            body_dict['timeUnit']=timeUnit
            body_dict['keywordGroups']=self.keywordGroups
            body_dict['device']=device
            body_dict['gender']=gender
            body_dict['ages']=ages

            body=str(body_dict).replace("'",'"') # ' 문자로는 에러가 발생해서 " 로 변환

            response_json = self.request_api(body)

            # 결과데이터중 'data' 와 'title'만 따로 DataFrame으로 저장
            response_results = pd.DataFrame()
            for data in response_json['results']:
                result=pd.DataFrame(data['data'])
                result['title']=data['title']
                result['gender']=gender # 기기 정보를 추가

                response_results = pd.concat([response_results,result])
            
            response_results_all = pd.concat([response_results_all,response_results])
            
        #title별로 그래프를 그리기 위한부분
        titles=response_results['title'].unique() 

        graph_data = {}
        for gender in genders:
            buf = BytesIO()
            plt.figure(figsize=(4,4))
            for title in titles:
                data=response_results_all.loc[(response_results_all['title']==title) 
                            & (response_results_all['gender']==gender),:]
                plt.plot(data['period'],data['ratio'],label=title)
                plt.xticks(rotation=90)
                plt.ylabel("검색량")
                plt.legend()
            if str(gender) == 'm':
                plt.title('MALE')
            elif str(gender) == 'f':
                plt.title('FEMALE')
            plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.3)  # 잘 맞게 조절
            plt.savefig(buf, format="png")
            graph_data[gender] = base64.b64encode(buf.getbuffer()).decode("ascii")
        
        return graph_data
        
    def get_data(self, startDate, endDate, timeUnit, device, ages, gender):
        """
        요청 결과 반환
        timeUnit - 'date', 'week', 'month'
        device - None, 'pc', 'mo'
        ages = [], ['1' ~ '11']
        gender = None, 'm', 'f'
        """

        # Request body
        body = json.dumps({
            "startDate": startDate,
            "endDate": endDate,
            "timeUnit": timeUnit,
            "keywordGroups": self.keywordGroups,
            "device": device,
            "ages": ages,
            "gender": gender
        }, ensure_ascii=False)
        
        # Results
        request = urllib.request.Request(self.url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        request.add_header("Content-Type","application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            # Json Result
            result = json.loads(response.read())
            
            df = pd.DataFrame(result['results'][0]['data'])[['period']]
            for i in range(len(self.keywordGroups)):
                tmp = pd.DataFrame(result['results'][i]['data'])
                tmp = tmp.rename(columns={'ratio': result['results'][i]['title']})
                df = pd.merge(df, tmp, how='left', on=['period'])
            self.df = df.rename(columns={'period': '날짜'})
            self.df['날짜'] = pd.to_datetime(self.df['날짜'])
            
        else:
            print("Error Code:" + rescode)
            
        return self.df
    
    def plot_daily_trend(self):
        """
        일 별 검색어 트렌드 그래프 출력
        """
        colList = self.df.columns[1:]
        n_col = len(colList)

        fig = plt.figure(figsize=(12,6))
        plt.title('일 별 검색어 트렌드', size=20, weight='bold')
        for i in range(n_col):
            sns.lineplot(x=self.df['날짜'], y=self.df[colList[i]], label=colList[i])
        plt.legend(loc='upper right')
        
        return fig
    
    def plot_monthly_trend(self):
        """
        월 별 검색어 트렌드 그래프 출력
        """
        df = self.df.copy()
        df_0 = df.groupby(by=[df['날짜'].dt.year, df['날짜'].dt.month]).mean().droplevel(0).reset_index().rename(columns={'날짜': '월'})
        df_1 = df.groupby(by=[df['날짜'].dt.year, df['날짜'].dt.month]).mean().droplevel(1).reset_index().rename(columns={'날짜': '년도'})

        df = pd.merge(df_1[['년도']], df_0, how='left', left_index=True, right_index=True)
        df['날짜'] = pd.to_datetime(df[['년도','월']].assign(일=1).rename(columns={"년도": "year", "월":'month','일':'day'}))
        
        colList = df.columns.drop(['날짜','년도','월'])
        n_col = len(colList)
                
        fig = plt.figure(figsize=(12,6))
        plt.title('월 별 검색어 트렌드', size=20, weight='bold')
        for i in range(n_col):
            sns.lineplot(x=df['날짜'], y=df[colList[i]], label=colList[i])
        plt.legend(loc='upper right')
        
        return fig


# import os
# import sys
# import urllib.request
# from define import const
# import json

# def search_data():
#     client_id = const.SEARCH_API_CLIENT_ID
#     client_secret = const.SEARCH_API_CLIENT_SECRET
#     search_data = make_temp_data()
#     print(search_data)
#     url = const.SEARCH_API_BASE_URL
#     body = json.dumps(search_data)

#     request = urllib.request.Request(url)
#     request.add_header("X-Naver-Client-Id",client_id)
#     request.add_header("X-Naver-Client-Secret",client_secret)
#     request.add_header("Content-Type","application/json")
#     response = urllib.request.urlopen(request, data=body.encode("utf-8"))
#     rescode = response.getcode()
#     if(rescode==200):
#         response_body = response.read()
#         print('')
#         print(response_body.decode('utf-8'))
#     else:
#         print("Error Code:" + rescode)


# def make_temp_data():
#     return {
#         'startDate' : '2017-01-01',
#         'endDate' : '2023-01-01',
#         'timeUnit' : 'month',
#         # 'keywordGroups' : [{"groupName":"한글","keywords":["한글","korean"]},{"groupName":"영어","keywords":["영어","english"]}],
#         'keywordGroups' : [{"groupName":"자동차","keywords":["현대","기아"]}],
#         'device' : 'pc',
#         'ages' : ["1","2"],
#         'gender' : 'f'
#     }