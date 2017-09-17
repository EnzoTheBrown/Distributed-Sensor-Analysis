from pyspark import SparkContext  
from pyspark.streaming import StreamingContext  
from pyspark.streaming.kafka import KafkaUtils  
from pyspark.sql import SparkSession
from pyspark.sql import Row
import pywt
import json  
import numpy as np
from simplemysql import SimpleMysql
import time


sc = SparkContext(appName="App")  
sc.setLogLevel("ERROR")

ssc = StreamingContext(sc, 5)  
kafkaStream = KafkaUtils.createStream(ssc, 'localhost:5181', 'test-consumer-group', {'camera':1})  

parsed = kafkaStream.map(lambda v: json.loads(v[1]))  
def avg(x, y):
    if y[1] > 0:
        return [x, y[0]/y[1]]
    else:
        return [x, None]

def load_in_base(rdd):
    pass

parsed.map(lambda l: [l['index'], [l['dist'], 1]])\
    .reduceByKey(lambda x, y: [x[0] + y[0], x[1] + y[1]])\
    .map(lambda x: avg(x[0], x[1])).pprint()



############### mysql ###################

db = SimpleMysql(
    host="127.0.0.1",
    db="ter",
    user="root",
    passwd="password",
    keep_alive=True # try and reconnect timedout mysql connections?
)


def insert_in_base(data):
    tmp = data.collect()
    if len(tmp) == 0 or len(tmp[0]) == 0:
        return data
    db.insert("wavelet", {'id': time.time(), 'data': json.dumps(tmp[0][1].tolist()), 'camera_index': tmp[0][0]})
   # print(db.getAll("wavelet", ["data", "id"], ("id - %s > 0 and camera_index=%s", [str(int(time.time()) - 3600), str(tmp[0][0])])))
    return data

def get_from_base(camera_index):
    print(db.getAll("wavelet", ["data", "id"]))
    return 3
#########################################, ("id - %s > 0 and camera_index=%s", [str(int(time.time()) - 3600), str(0)])

def display_(x):
    print(x)
    return x

wavelet = parsed\
    .map(lambda l: [l['index'], [l['dist']]])\
    .reduceByKey(lambda x, y: x + y)\
    .map(lambda x: [x[0], pywt.dwt(x[1], 'db1')[1]])\
    .pprint()
# 
# # add to database
# wavelet\
#     .foreachRDD(insert_in_base)
# 
# wavelet\
#     .map(lambda x: get_from_base(x[0])).pprint()


# .map(lambda x: db.insert("wavelet", {"id":0, "data":json.dumps(range(1000))}))\

# .foreachRDD(lambda rdd: print(rdd))
# 
ssc.start()  
ssc.awaitTermination()  


