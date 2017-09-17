from kafka import KafkaProducer


import json
import time

from VideoAnalysis.get_stream_from_video import HandleStream
from VideoAnalysis.get_basic_data import *



video_link='people_walking.mp4'
previous_flows = [0]*500

stream = HandleStream(video_link)

producer = KafkaProducer(bootstrap_servers='localhost:9092', api_version=(0,10))
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    data, previous_flows = preprocessing(stream, previous_flows)
    producer.send(data)
    time.sleep(0.2)

    


