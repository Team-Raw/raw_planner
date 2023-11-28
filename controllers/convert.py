from io import BytesIO
import pandas as pd

from define import const
from api import searchTrend, searchRelated

def trend_convert(input_value, start_date, end_date):
    keyword_group_set = {
        'keyword_group_1': {'groupName': input_value, 'keywords': [input_value]},
    }

    # API 인증 정보 설정
    client_id = const.SEARCH_API_CLIENT_ID
    client_secret = const.SEARCH_API_CLIENT_SECRET

    # 요청 파라미터 설정
    startDate = start_date
    endDate = end_date
    timeUnit = 'month'
    device = ''
    ages = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    gender = ''

    # 데이터 프레임 정의
    search_trend_api = searchTrend.NaverDataLabOpenAPI(client_id=client_id, client_secret=client_secret)

    search_trend_api.add_keyword_groups(keyword_group_set['keyword_group_1'])

    # 데이터 요청
    age_graph_data = search_trend_api.get_result_age(startDate, endDate, timeUnit, device, ages, gender)
    device_graph_data = search_trend_api.get_result_device(startDate, endDate, timeUnit, device, ages, gender)
    gender_graph_data = search_trend_api.get_result_gender(startDate, endDate, timeUnit, device, ages, gender)

    return age_graph_data, device_graph_data, gender_graph_data

    # df = search_trend_api.get_data(startDate, endDate, timeUnit, device, ages, gender)
    #print(df.head())
    #fig_1 = search_trend_api.plot_daily_trend()

    #buf = BytesIO()
    #fig_1.savefig(buf, format="png")
    #data = base64.b64encode(buf.getbuffer()).decode("ascii")

    #return data

def related_convert(input_value):
    hintKeywords=[]
    hintKeywords.append(input_value)

    related_data = searchRelated.getresults(hintKeywords)
    related_data['monthlyPcQcCnt'] = pd.to_numeric(related_data['monthlyPcQcCnt'], errors='coerce')
    top_10_df = related_data.sort_values(by='monthlyPcQcCnt', ascending=False).head(10)

    monthlyPcQcCnt = top_10_df['monthlyPcQcCnt'].to_string(index=False, header=False)
    monthlyPcQcCnt_list = monthlyPcQcCnt.split('\n')
    monthlyPcQcCnt_dict = {
        '1': int(float(monthlyPcQcCnt_list[0].strip())),
        '2': int(float(monthlyPcQcCnt_list[1].strip())),
        '3': int(float(monthlyPcQcCnt_list[2].strip())),
        '4': int(float(monthlyPcQcCnt_list[3].strip())),
        '5': int(float(monthlyPcQcCnt_list[4].strip())),
        '6': int(float(monthlyPcQcCnt_list[5].strip())),
        '7': int(float(monthlyPcQcCnt_list[6].strip())),
        '8': int(float(monthlyPcQcCnt_list[7].strip())),
        '9': int(float(monthlyPcQcCnt_list[8].strip())),
        '10': int(float(monthlyPcQcCnt_list[9].strip())),
    }

    relKeyword = top_10_df['relKeyword'].to_string(index=False, header=False)
    relKeyword_list = relKeyword.split('\n')
    relKeyword_dict = {
        '1': relKeyword_list[0].strip(),
        '2': relKeyword_list[1].strip(),
        '3': relKeyword_list[2].strip(),
        '4': relKeyword_list[3].strip(),
        '5': relKeyword_list[4].strip(),
        '6': relKeyword_list[5].strip(),
        '7': relKeyword_list[6].strip(),
        '8': relKeyword_list[7].strip(),
        '9': relKeyword_list[8].strip(),
        '10': relKeyword_list[9].strip(),
    }

    monthlyMobileQcCnt_dict, mo_relKeyword_dict = get_mobile_data(related_data)

    return monthlyPcQcCnt_dict, relKeyword_dict, monthlyMobileQcCnt_dict, mo_relKeyword_dict

def get_mobile_data(related_data):
    related_data['monthlyMobileQcCnt'] = pd.to_numeric(related_data['monthlyMobileQcCnt'], errors='coerce')
    top_10_df = related_data.sort_values(by='monthlyMobileQcCnt', ascending=False).head(10)

    monthlyMobileQcCnt = top_10_df['monthlyMobileQcCnt'].to_string(index=False, header=False)
    monthlyMobileQcCnt_list = monthlyMobileQcCnt.split('\n')
    monthlyMobileQcCnt_dict = {
        '1': int(float(monthlyMobileQcCnt_list[0].strip())),
        '2': int(float(monthlyMobileQcCnt_list[1].strip())),
        '3': int(float(monthlyMobileQcCnt_list[2].strip())),
        '4': int(float(monthlyMobileQcCnt_list[3].strip())),
        '5': int(float(monthlyMobileQcCnt_list[4].strip())),
        '6': int(float(monthlyMobileQcCnt_list[5].strip())),
        '7': int(float(monthlyMobileQcCnt_list[6].strip())),
        '8': int(float(monthlyMobileQcCnt_list[7].strip())),
        '9': int(float(monthlyMobileQcCnt_list[8].strip())),
        '10': int(float(monthlyMobileQcCnt_list[9].strip())),
    }

    mo_relKeyword = top_10_df['relKeyword'].to_string(index=False, header=False)
    mo_relKeyword_list = mo_relKeyword.split('\n')
    mo_relKeyword_dict = {
        '1': mo_relKeyword_list[0].strip(),
        '2': mo_relKeyword_list[1].strip(),
        '3': mo_relKeyword_list[2].strip(),
        '4': mo_relKeyword_list[3].strip(),
        '5': mo_relKeyword_list[4].strip(),
        '6': mo_relKeyword_list[5].strip(),
        '7': mo_relKeyword_list[6].strip(),
        '8': mo_relKeyword_list[7].strip(),
        '9': mo_relKeyword_list[8].strip(),
        '10': mo_relKeyword_list[9].strip(),
    }

    return monthlyMobileQcCnt_dict, mo_relKeyword_dict