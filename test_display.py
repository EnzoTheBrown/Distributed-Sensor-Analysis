from pyspark import SparkContext  
from pyspark.streaming import StreamingContext  
from pyspark.streaming.kafka import KafkaUtils  
from pyspark.sql import SparkSession
from pyspark.sql import Row
import json  



sc = SparkContext(appName="App")  
sc.setLogLevel("ERROR")

ssc = StreamingContext(sc, 1)  
kafkaStream = KafkaUtils.createStream(ssc, 'localhost:5181', 'test-consumer-group', {'camera':1})  

parsed = kafkaStream.map(lambda v: json.loads(v[1]))
parsed.count().pprint()

ssc.start()  
ssc.awaitTermination()  


