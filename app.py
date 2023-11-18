# /app.py
from flask import Flask, render_template, request

#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/',methods=('GET', 'POST')) # 접속하는 url
def index():
    if request.method == "POST":
        # user=request.form['user'] # 전달받은 name이 user인 데이터
        print(request.form.get('user')) # 안전하게 가져오려면 get
        user = request.form.get('user')
        data = {'level': 60, 'point': 360, 'exp': 45000}
        return render_template('index.html', user=user, data=data)
    elif request.method == "GET":
        user = "반원"
        data = {'level': 60, 'point': 360, 'exp': 45000}
        return render_template('index.html', user=user, data=data)


if __name__=="__main__":
    app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    # app.run(host="127.0.0.1", port="5000", debug=True)