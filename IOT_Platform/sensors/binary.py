import random, time
from confluent_kafka import Consumer, KafkaError, Producer
from random import choices

population = [1, 2]
weights = [0.9, 0.1]
p = Producer({'bootstrap.servers': "localhost:9092"})
while True:
    ch= choices(population, weights)[0]
    if ch==1:
        value= 0
    else:
        value= 1
    
    p.produce("binary", str(value).encode('utf-8'))
    p.poll(0)
    print(value)
    time.sleep(5)
