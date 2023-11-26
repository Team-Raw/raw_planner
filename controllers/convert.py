from io import BytesIO
import base64
import pandas as pd

from define import const
from api import searchTrend, searchRelated

def trend_convert():
    keyword_group_set = {
        'keyword_group_1': {'groupName': "애플", 'keywords': ["애플"]},
        'keyword_group_2': {'groupName': "아마존", 'keywords': ["아마존"]},
        # 'keyword_group_3': {'groupName': "구글", 'keywords': ["구글"]},
        # 'keyword_group_4': {'groupName': "테슬라", 'keywords': ["테슬라"]},
        # 'keyword_group_5': {'groupName': "페이스북", 'keywords': ["페이스북"]}
    }

    # API 인증 정보 설정
    client_id = const.SEARCH_API_CLIENT_ID
    client_secret = const.SEARCH_API_CLIENT_SECRET

    # 요청 파라미터 설정
    startDate = "2023-01-01"
    endDate = "2023-11-25"
    timeUnit = 'date'
    device = ''
    ages = []
    gender = ''

    # 데이터 프레임 정의
    search_trend_api = searchTrend.NaverDataLabOpenAPI(client_id=client_id, client_secret=client_secret)

    search_trend_api.add_keyword_groups(keyword_group_set['keyword_group_1'])
    search_trend_api.add_keyword_groups(keyword_group_set['keyword_group_2'])
    # search_trend_api.add_keyword_groups(keyword_group_set['keyword_group_3'])
    # search_trend_api.add_keyword_groups(keyword_group_set['keyword_group_4'])
    # search_trend_api.add_keyword_groups(keyword_group_set['keyword_group_5'])

    df = search_trend_api.get_data(startDate, endDate, timeUnit, device, ages, gender)
    print(df.head())
    fig_1 = search_trend_api.plot_daily_trend()

    buf = BytesIO()
    fig_1.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data

def related_convert(request):
    hintKeywords=[]
    input_value = request.form['input']
    hintKeywords.append(input_value)

    related_data = searchRelated.getresults(hintKeywords)
    related_data['monthlyPcQcCnt'] = pd.to_numeric(related_data['monthlyPcQcCnt'], errors='coerce')
    top_10_df = related_data.sort_values(by='monthlyPcQcCnt', ascending=False).head(10)
    result = top_10_df['relKeyword'].to_string(index=False, header=False)
    result_list = result.split('\n')
    result_dict = {
        '1': result_list[0].strip(),
        '2': result_list[1].strip(),
        '3': result_list[2].strip(),
        '4': result_list[3].strip(),
        '5': result_list[4].strip(),
        '6': result_list[5].strip(),
        '7': result_list[6].strip(),
        '8': result_list[7].strip(),
        '9': result_list[8].strip(),
        '10': result_list[9].strip(),
    }

    return result_dict