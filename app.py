from flask import Flask, render_template, request
from api import searchTrend, searchRelated
from controllers import convert
# from flask_restx import Api, Resource, reqparse

app = Flask(__name__)
# api = Api(app, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs")
# search_api = api.namespace('search', description='데이터 조회 API')

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

if __name__=="__main__":
    app.run(debug=True)
    # app.run(host="127.0.0.1", port="5000", debug=True)