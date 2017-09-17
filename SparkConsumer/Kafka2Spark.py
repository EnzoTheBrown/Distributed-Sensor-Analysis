from pyspark import SparkContext  
from pyspark.streaming import StreamingContext  
from pyspark.streaming.kafka import KafkaUtils  

import json  


sc = SparkContext(appName="DSA")  
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 5)

kafkaStream = KafkaUtils.createStream(ssc, 'localhost:5181', 'consumer grp here', {'camera':1})
parsed.count().pprint()  

