
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from settings import *
import sys

MASTER = "spark://{}:7077".format(settings.MASTER_SPARK)
PUBLIC_IP = "{}:2181".format(settings.MASTER_PUBLIC_IP)
topic = sys.argv[1]
partitions = sys.argv[2]

# Create a local StreamingContext with two working thread and batch interval of 2 second
sc = SparkContext(MASTER, "MyTest")
ssc = StreamingContext(sc, 1)

kafkaStream = KafkaUtils.createStream(ssc, PUBLIC_IP, "flask", {topic: partitions})

messages = kafkaStream.map(lambda xs:xs)
messages.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
