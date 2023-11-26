from flask import Flask, render_template, request
from api import searchTrend, searchRelated
from controllers import convert

app = Flask(__name__)

# HTML Render
@app.route('/',methods=('GET', 'POST'))
def index():
    return render_template('index.html')

# 구현필요
# @app.route('/service',methods=('GET', 'POST'))
# def service():
#     return render_template('service.html')

@app.route('/search',methods=('GET', 'POST'))
def search():
    return render_template('search.html')

@app.route('/search_result',methods=('GET', 'POST'))
def result():
    if request.method == 'POST':
        # hintKeywords=[]
        # input_value = request.form['input']
        # hintKeywords.append(input_value)
        # result = searchRelated.getresults(hintKeywords)
        # print(result)
        data = convert.trend_convert()
        return render_template('search_result.html', result=f"<img src='data:image/png;base64,{data}'/>")
    return render_template('search_result.html')

# API
@app.route('/search/trend',methods=('GET', 'POST'))
def search_trend():
    searchTrend.search_data()
    return render_template('search.html')

@app.route('/search/related',methods=('GET', 'POST'))
def search_relative():
    hintKeywords=['강원도풀빌라']
    result = searchRelated.getresults(hintKeywords)
    return render_template('search.html', result=result)



#########################################################TEST CODE##################################################################
from matplotlib import pyplot as plt
import numpy as np

@app.route('/test',methods=('GET', 'POST'))
def test_render():
    x = np.arange(1,10)
    y = x*5

    plt.plot(x,y)
    plt.show()

    return render_template('temp/test.html', result=result)

@app.route('/trend_test',methods=('GET', 'POST'))
def index_test():
    data = convert.trend_convert()

    return render_template('temp/index_test.html', result=f"<img src='data:image/png;base64,{data}'/>")


if __name__=="__main__":
    app.run(debug=True)
    # app.run(host="127.0.0.1", port="5000", debug=True)