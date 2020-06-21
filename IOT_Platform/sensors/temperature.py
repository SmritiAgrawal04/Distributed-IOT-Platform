import random, time
from confluent_kafka import Consumer, KafkaError, Producer
from random import choices

population = [1, 2, 3, 4]
weights = [0.6, 0.2, 0.15, 0.05]
p = Producer({'bootstrap.servers': "localhost:9092"})
while True:
    ch= choices(population, weights)[0]
    if ch==1:
        value= random.randrange(60, 100)
    elif ch==2:
        value= random.randrange(10, 59)
    elif ch==3:
        value= random.randrange(101, 200)
    else:
        value= random.randrange(201, 500)
    
    p.produce("temp", str(value).encode('utf-8'))
    p.poll(0)
    print(value)
    time.sleep(30)
