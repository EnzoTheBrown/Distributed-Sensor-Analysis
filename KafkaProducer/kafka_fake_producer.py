from kafka import KafkaProducer

import json
import time
import random
from scipy.spatial import distance

def create_rand():
    return [random.randrange(0, 1000)]*5
previous_flow = create_rand()


producer = KafkaProducer(bootstrap_servers='localhost:9092', api_version=(0,10))
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    flow = create_rand()
    data = {'index': random.randrange(4), 'dist': distance.euclidean(flow, previous_flow) }
    producer.send('camera', data)
    previous_flow = flow
    time.sleep(0.2)

    


