from confluent_kafka import Consumer, KafkaError, Producer
import time, sys, json

def run_actionNotification(value):
    print(value)

c = Consumer({'bootstrap.servers': "localhost:9092", 'group.id': sys.argv[1], 'auto.offset.reset': 'latest'})
c.subscribe(["binary"])

while True:
    msg = c.poll(1.0)

    if msg is None or msg.error():
        continue

    value= int((msg.value()).decode('utf-8'))
    print("****value= ", value, "******")
    # run_actionNotification(value)