from flask import Flask, render_template, request
from api import searchTrend, searchRelated
from controllers import convert
from flask_restx import Api, Resource, fields

app = Flask(__name__)

# HTML Render
@app.route('/',methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@app.route('/service',methods=('GET', 'POST'))
def service():
    return render_template('service.html')

@app.route('/search',methods=('GET', 'POST'))
def search():
    return render_template('search.html')

@app.route('/search_result',methods=('GET', 'POST'))
def result():
    if request.method == 'POST':
        monthlyPcQcCnt_dict, relKeyword_dict, monthlyMobileQcCnt_dict, mo_relKeyword_dict = convert.related_convert(request.form['input'])
        age_graph_data, device_graph_data, gender_graph_data = convert.trend_convert(request.form['input'])
        return render_template('search_result.html', monthlyPcQcCnt_dict=monthlyPcQcCnt_dict, 
                                relKeyword_dict=relKeyword_dict, 
                                monthlyMobileQcCnt_dict=monthlyMobileQcCnt_dict, 
                                mo_relKeyword_dict=mo_relKeyword_dict,
                                age_graph_data=age_graph_data, 
                                device_graph_data=device_graph_data, 
                                gender_graph_data=gender_graph_data)
    return render_template('search_result.html')

api = Api(app, version='1.0', title='Trendy API 문서', description='API Documentation', doc="/api-docs")
search_api = api.namespace('/', description='페이지 조회 요청 API')

# Define your routes using the @namespace.route decorator
@search_api.route('/')
class Index(Resource):
    def get(self):
        """메인페이지 요청"""
        return {'message': 'This is a test endpoint', 'parameters':'dd'}
    
@search_api.route('/service')
class Service(Resource):
    def get(self):
        """서비스 소개 페이지 요청"""
        return {'message': 'This is a test endpoint'}
    
@search_api.route('/search')
class Search(Resource):
    def get(self):
        """검색 페이지 요청"""
        return {'message': 'This is a test endpoint'}
    
@search_api.route('/search_result')
class SearchResult(Resource):
    def get(self):
        """검색 데이터 조회 페이지 요청"""
        return {'message': 'This is a test endpoint'}
    
    def post(self):
        """검색 데이터 요청하여 연관검색어, 트랜드 그래프 리턴"""
        return {'message': 'This is a test endpoint'}

if __name__=="__main__":
    app.run(debug=True)
    # app.run(host="127.0.0.1", port="5000", debug=True)