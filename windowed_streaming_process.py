import os  
os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars ~/spark/jars/spark-streaming-kafka.jar pyspark-shell'  
from pyspark import SparkContext  
from pyspark.streaming import StreamingContext  
from pyspark.streaming.kafka import KafkaUtils  
import json 


def createContext():  
    sc = SparkContext(appName="windowed_streaming")
    sc.setLogLevel("WARN")
    ssc = StreamingContext(sc, 5)

    # Define Kafka Consumer
    kafkaStream = KafkaUtils.createStream(ssc, '192.168.237.56:5181', 'test-consumer-group', {'camera':1})

    ## --- Processing
    # Extract tweets
    parsed = kafkaStream.map(lambda v: json.loads(v[1]))

    # Count number of tweets in the batch
    count_this_batch = kafkaStream.count().map(lambda x:('ppl counted in this batch: %s' % x))

    # Count by windowed time period
    count_windowed = kafkaStream.countByWindow(60,5).map(lambda x:('ppl total (One minute rolling count): %s' % x))

    # Get authors
    dist_dstream = parsed.map(lambda line: line['dist'])

    # Count each value and number of occurences 
    count_values_this_batch = dist_dstream.countByValue()\
                                .transform(lambda rdd:rdd\
                                  .sortBy(lambda x:-x[1]))\
                              .map(lambda x:"dist counts this batch:\tValue %s\tCount %s" % (x[0],x[1]))

    # Count each value and number of occurences in the batch windowed
    count_values_windowed = dist_dstream.countByValueAndWindow(60,5)\
                                .transform(lambda rdd:rdd\
                                  .sortBy(lambda x:-x[1]))\
                            .map(lambda x:"ppl counts (One minute rolling):\tValue %s\tCount %s" % (x[0],x[1]))

    # Write total tweet counts to stdout
    # Done with a union here instead of two separate pprint statements just to make it cleaner to display
    count_this_batch.union(count_windowed).pprint()

    # Write tweet author counts to stdout
    count_values_this_batch.pprint(5)
    count_values_windowed.pprint(5)

    return ssc

ssc = StreamingContext.getOrCreate('/tmp/checkpoint_v01',lambda: createContext())  
ssc.start()  
ssc.awaitTermination() 




