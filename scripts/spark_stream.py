from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from settings import *
import sys

# print settings.MASTER_SPARK

# MASTER = "spark://{}:7077".format(settings.MASTER_SPARK)
# PUBLIC_IP = "{}:2181".format(settings.MASTER_PUBLIC_IP)
topic = sys.argv[1]
partitions = sys.argv[2]
MASTER = "spark://{}:7077".format("ec2-54-173-157-255.compute-1.amazonaws.com")
PUBLIC_IP = "{}:2181".format(sys.argv[3])

# Create a local StreamingContext with two working thread and batch interval of 2 second
sc = SparkContext(MASTER, "MyTest1")
ssc = StreamingContext(sc, 1)

kafkaStream = KafkaUtils.createStream(ssc, PUBLIC_IP, "flask", {topic: partitions})

messages = kafkaStream.map(lambda xs:xs)
messages.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
