import random
import sys, os
import six
from datetime import datetime
from kafka.client import KafkaClient
from kafka.producer import KeyedProducer

class Producer(object):

    def __init__(self, addr):
        self.client = KafkaClient(addr)
        self.producer = KeyedProducer(self.client)

    def open_save(self, fileName):
        log_file = open(fileName, "w")
        log_file.close()
        return log_file

    def create_topic(self, topic):
        script = "/usr/local/kafka/bin/kafka-topics.sh"
        os.system("{} --create --zookeeper localhost:2181 --topic {} --partitions {} --replication-factor 2".format(script, topic, "4"))
        return "topic {} created".format(topic)

    def produce_msgs(self, source_symbol, topic):
        server_topics = self.client.topic_partitions
        if topic not in server_topics:
          self.create_topic(topic)
        price_field = random.randint(800,1400)
        cities = ["Barcelona", "Philadelphia", "Honolulu",
                  "Atlanta", "Miami", "Chicago", "SF", "LA", "NYC",
                  "Houston", "Paris", "London", "Tokyo"]
        msg_cnt = 0
        log_file = open("input1/{}.csv".format(topic), "a")
        while True:
            time_field = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
            location_field = random.choice(cities)
            price_field += random.randint(-10, 10)/10.0
            str_fmt = "{},{},{},{}"
            message_info = str_fmt.format(source_symbol,
                                          time_field,
                                          location_field,
                                          price_field)
            print message_info
            log_file.write("{}\n".format(message_info))
            self.producer.send_messages(topic, source_symbol, message_info)
            msg_cnt += 1
            if msg_cnt > 200000:
                log_file.close()
                self.producer.stop()
                break

if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])
    partition_key = str(args[2])
    topic = str(args[3])
    prod = Producer(ip_addr)
    prod.open_save("input1/{}.csv".format(topic))
    prod.produce_msgs(partition_key, topic)
# http://stackoverflow.com/questions/4256107/running-bash-commands-in-python
