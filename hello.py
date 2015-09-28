from flask import Flask
from flask import Flask, render_template
import os

from settings import *

app = Flask(__name__)

@app.route("/")
@app.route('/index')
def hello():
    return "Hello World!"

@app.route("/case/<id>/")
def case(id):
    return id


@app.route("/test/<id>/")
def test(id):
    return id

@app.route("/demo")
@app.route("/test")
def create_test():
	return render_template("demo.html")

@app.route("/demo/time")
def api_one():
	return "time"

@app.route("/api/count")
def api_count(topic):
    # open topic_testId
    # count number of lines in the file
    return "count"



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


