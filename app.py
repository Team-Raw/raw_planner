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
        related_data = convert.related_convert(request.form['input'])
        trend_data = convert.trend_convert(request.form['input'])
        return render_template('search_result.html', related_data=related_data, trend_data=trend_data)
    return render_template('search_result.html')

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

if __name__=="__main__":
    app.run(debug=True)
    # app.run(host="127.0.0.1", port="5000", debug=True)