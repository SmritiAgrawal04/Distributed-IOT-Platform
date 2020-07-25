import random, time, json
from confluent_kafka import Consumer, KafkaError, Producer
from random import choices

population = [1, 2, 3]
weights = [0.6, 0.2, 0.2]
p = Producer({'bootstrap.servers': "localhost:9092"})
while True:
    ch= choices(population, weights)[0]
    if ch==1:
        strength= random.randrange(30, 70)
        seats= random.randrange(150, 250)
    elif ch==2:
        strength= random.randrange(50, 100)
        seats= random.randrange(100, 150)
    else:
        strength= random.randrange(30, 50)
        seats= random.randrange(80, 100)

    class_data= {'strength': strength, 'seats': seats}
    class_data= json.dumps(class_data)
    
    p.produce("numeric", class_data.encode('utf-8'))
    p.poll(0)
    # print(class_data)
    time.sleep(60)
