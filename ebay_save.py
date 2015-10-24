# connect with spark streaming
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import pyspark_cassandra
from pyspark_cassandra import streaming
import settings


sc = SparkContext("spark://MASTER:7077", "TestSpark")
ssc = StreamingContext(sc, 60)

kafkaStream = KafkaUtils.createStream(ssc, "IP_ADDRESS", "topic", {"justsoldonebay": 4})
raw = kafkaStream.map(lambda kafkaS: kafkaS[1].split(";") )
#raw.pprint()

count = raw.map(lambda x: len(x))
count.pprint()

ebay_listing = raw.map(lambda x: {
      "starttime": x[0],
      "endtime": x[1],
      "view_item_url": x[2],
      "shoeid": x[3],
      "shoe": x[4],
      "price": round(float(x[5]), 2),
      "gender": x[7],
      "gallery_url": x[8],
      "location": x[9],
      "title": x[10],
      "zipcode": x[6],
      "zipcode2": x[11] })
        
ebay_listing.pprint()

ebay_listing.saveToCassandra("spark_pond", "justsoldonebay")

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
