from flask import Flask, render_template, jsonify, request, Response
from flask import make_response
from json import dumps
import os
import settings
from settings import *
import subprocess
from cassandra.cluster import Cluster
from datetime import datetime
import json
from operator import itemgetter
from pyzipcode import ZipCodeDatabase

app = Flask(__name__)

# Connect to Cassandra
cluster = Cluster(['54.164.65.18'])
session = cluster.connect('spark_pond')
session.default_timeout = 30 # 30 seconds


@app.route("/")
@app.route('/index')
def home():
  return render_template("home.html")

# create topic
@app.route("/test/spark/create/<topic>/")
def create_topic(topic):
    script = "/usr/local/kafka/bin/kafka-topics.sh"
    os.system("{} --create --zookeeper localhost:2181 --topic {} --partitions {} --replication-factor 2".format(script, topic, "4"))
    return "topic {} created".format(topic)

@app.route("/test/spark/produce/<topic>/")
@app.route("/test/spark/stream/<topic>/")
def start_spark_test(topic):
    # python test/a_producer.py `hostname` 1 test_a_11
    kafka_script = "kafka_producer1.py"
    hostname = settings.MASTER_PUBLIC_IP
    os.system("python {} {} 4 {}".format(kafka_script, hostname, topic))

    # spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.5.0 processing/spark_test.py
    spark_script = "spark_stream.py"
    package = "--packages org.apache.spark:spark-streaming-kafka_2.10:1.5.0"
    os.system("spark-submit {} {} {} 1".format(package, spark_script, topic))
    return redirect("http://de.katychuang.me:5000/latest", code=302)

@app.route("/latest/<filename>")
def latest(filename):
    st = os.stat("input1/{}.csv".format(filename))
    # TODO Make this show a form with a list of available topics/tests
    context = {'data': st}
    return render_template("latest.html", **context)

@app.route("/test/<id>/")
def test(id):
    return id

@app.route("/demo")
def x():
    x = '<a href="http://de.katychuang.me:5000/chart/latency/spark_1m">spark latency</a>'
    x += '<br>'
    x += '<a href="http://de.katychuang.me:5000/map4">map</a>'
    return x

@app.route("/mockup")
def create_test():
	return render_template("demo.html")

@app.route("/api/zip")
def zip():
    stmt = "SELECT shoeid, starttime, endtime, shoe, zipcode, price from justsoldonebay;"
    response = session.execute(stmt)
    j = []
    zcdb = ZipCodeDatabase()
    for dot in response:
        z = {}
        z["zip"] = dot.zipcode
        z["id"] = dot.shoeid
        z["shoe"] = dot.shoe
        z["sold"] = dot.endtime
        z["price"] = dot.price
        try:
            zipcode = zcdb[dot.zipcode]
            z["ll"] = [zipcode.longitude,zipcode.latitude]
            z["city"] = zipcode.city
            z["lat"] = zipcode.latitude
            z["lon"] = zipcode.longitude
        except:
          pass
        j.append(z)

    return make_response(dumps(j))


@app.route("/jordan-v-yeezy")
@app.route("/map4") #highmaps
def map4():
    return render_template("map4.html")

@app.route("/api/time/storm")
def time_storm():
  timestamps = []
  f = open('storm_test/time1_test.txt', 'r')
#  f.read()
  for line in f:
    timestamps.append(line[:-1])
  return make_response(dumps(timestamps))

@app.route("/api/time/<topic>")
def api_one(topic):
    # 3 seconds batch interval
    stmt = "SELECT testid, time1, delta FROM spark_1m limit 5000"
    response = session.execute(stmt)
    print type(response)
    response.sort(key=itemgetter(1))
    tmp_point = []
    for ping in response:
        time = ping.time1
        delta = ping.delta
        tmp_point.append([time,delta])
         
    return make_response(dumps(tmp_point))

@app.route("/api/latency/spark_1m")
def api_two():
    # 3 seconds batch interval
    stmt = "SELECT testid, time1, delta FROM spark_1m"
    response = session.execute(stmt)
    tmp_point = []
    for ping in response:
        tmp_point.append([ping.time1,ping.delta])
    return make_response(dumps(tmp_point))

@app.route("/chart/storm-v-spark")
def chart_ss():
  return render_template("charts.html")

@app.route("/chart/latency/<topic>")
@app.route("/chart/time")
def chart_time(topic):
    return render_template("line_chart.html")

@app.route("/api/throughput/<test>/<topic>")
def api_count(test, topic):
    # http://de.katychuang.me:5000/api/count/input1/test_a_100000000
    # open topic_testId
    # count number of lines in the file
    # st = os.stat("input1/{}.csv".format(topic))
    return  ""

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


