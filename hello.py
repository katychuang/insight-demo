from flask import Flask
from flask import Flask, render_template
import os

from settings import *

app = Flask(__name__)

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


