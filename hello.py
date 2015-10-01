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

app = Flask(__name__)

# Connect to Cassandra
cluster = Cluster(['54.164.65.18'])
session = cluster.connect('spark_pond')
session.default_timeout = 30 # 30 seconds


@app.route("/")
@app.route('/index')
def hello():
    return "Hello World!"

# create topic
@app.route("/test/spark/create/<topic>/")
def create_topic(topic):
    script = "/usr/local/kafka/bin/kafka-topics.sh"
    os.system("{} --create --zookeeper localhost:2181 --topic {} --partitions {} --replication-factor 2".format(script, topic, "4"))
    # send confirmation
    return "topic created"

@app.route("/test/spark/produce/<topic>/")
def start_test(topic):
    # python test/a_producer.py `hostname` 1 test_a_11
    script = "kafka_producer1.py"
    hostname = settings.MASTER_PUBLIC_IP
    os.system("python {} {} {}".format(script, hostname, topic))

@app.route("/test/spark/consume/<topic>")
def read_spark_stream(topic):
 # spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.5.0 processing/spark_test.py
    hostname = settings.MASTER_PUBLIC_IP 
    script = "spark_stream.py"
    os.system("python {} {} 1 {}".format(script, hostname, topic))
    return "sent"


@app.route("/test/<id>/")
def test(id):
    return id

@app.route("/demo")
@app.route("/test")
def create_test():
	return render_template("demo.html")

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

@app.route("/chart/latency/<topic>")
@app.route("/chart/time")
def chart_time(topic):
    return render_template("line_chart.html")

@app.route("/api/throughput/<test>/<topic>")
def api_count(test, topic):
    # http://de.katychuang.me:5000/api/count/input1/test_a_100000000
    # open topic_testId
    # count number of lines in the file
    return "count"



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


