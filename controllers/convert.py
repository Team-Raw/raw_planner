import base64
from io import BytesIO
from matplotlib.figure import Figure

from define import const
from api import searchTrend

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