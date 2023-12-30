import pandas as pd

import matplotlib.pyplot as plt
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
        keyword_gorup = {
            'groupName': group_dict['groupName'],
            'keywords': group_dict['keywords']
        }
        
        self.keywordGroups.append(keyword_gorup)
        print(f">>> Num of keywordGroups: {len(self.keywordGroups)}")

    def set_ages_info(self, startDate, endDate, timeUnit, device, ages, gender):
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

        return response_results_all
    
    def set_device_info(self, startDate, endDate, timeUnit, devices, ages, gender):
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

        return response_results, response_results_all

    def set_gender_info(self, startDate, endDate, timeUnit, device, ages, genders):
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

        return response_results, response_results_all

    # 연령별 그래프
    def get_age_graph(self, startDate, endDate, timeUnit, device, ages, gender):

        age_conv={'1':'0∼12세','2':'13∼18세','3':'19∼24세','4':'25∼29세','5':'30∼34세',
            '6':'35∼39세','7':'40∼44세','8':'45∼49세','9':'50∼54세','10':'55∼59세','11':'60세 이상'}

        response_results_all = self.set_ages_info(startDate, endDate, timeUnit, device, ages, gender)
            
        #title별로 그래프를 그리기 위한부분
        titles = response_results_all['title'].unique()

        buf = BytesIO()
        plt.figure(figsize=(10, 6))  # 가로 10, 세로 6의 크기로 그림 생성

        for age in ages:
            for title in titles:
                data = response_results_all.loc[(response_results_all['title'] == title)
                                                & (response_results_all['age'] == age), :]
                plt.plot(data['period'], data['ratio'], label=f"{age_conv[age]}")

        plt.xticks(rotation=90)
        plt.ylabel("검색량")
        plt.legend(bbox_to_anchor=(1,1))
        plt.title("연령대별 검색량 추이")
        plt.subplots_adjust(left=0.1, right=0.7, top=0.9, bottom=0.3)  # 잘 맞게 조절
        plt.savefig(buf, format="png")
        graph_data = base64.b64encode(buf.getbuffer()).decode("ascii")

        return graph_data
    
    # 기기별 그래프
    def get_device_graph(self, startDate, endDate, timeUnit, device, ages, gender):
        devices = ['pc', 'mo']

        response_results, response_results_all = self.set_device_info(startDate, endDate, timeUnit, devices, ages, gender)

        #title별로 그래프를 그리기 위한부분
        titles=response_results['title'].unique() 

        graph_data = {}
        for device in devices:
            buf = BytesIO()
            plt.figure(figsize=(4,4))
            for title in titles:
                data=response_results_all.loc[(response_results_all['title']==title) 
                            & (response_results_all['device']==device),:]
                plt.bar(data['period'],data['ratio'],label=title, color='orange')
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
    def get_gender_graph(self, startDate, endDate, timeUnit, device, ages, gender):
        genders = ['m', 'f']

        response_results, response_results_all = self.set_gender_info(startDate, endDate, timeUnit, device, ages, genders)

        #title별로 그래프를 그리기 위한부분
        titles=response_results['title'].unique() 

        graph_data = {}
        for gender in genders:
            buf = BytesIO()
            plt.figure(figsize=(4,4))
            for title in titles:
                data=response_results_all.loc[(response_results_all['title']==title) 
                            & (response_results_all['gender']==gender),:]
                plt.bar(data['period'],data['ratio'],label=title, color='salmon')
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