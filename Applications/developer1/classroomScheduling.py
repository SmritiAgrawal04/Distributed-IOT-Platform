from confluent_kafka import Consumer, KafkaError, Producer
import time, sys, json, os
from datetime import datetime

p = Producer({'bootstrap.servers': "localhost:9092"})

def run_actionNotify(class_data):
	message= "The class {} had a Class Strength= {} and Number of Seats= {} of your {} at {}".format(sys.argv[8] ,class_data['strength'], class_data['seats'], sys.argv[3], str(datetime.now()))

	notify_data= {'notify_type': "message",
				  'app_name' : sys.argv[2],
				  'service' : sys.argv[3],
				  'username' : sys.argv[4],
				  'phone_number' : sys.argv[5],
				  'email' : sys.argv[6],
				  'firstname' : sys.argv[7],
				  'message' : message
	}

	notify_data= json.dumps(notify_data)
	p.produce('notify', notify_data.encode('utf-8'))
	p.poll(0)

c = Consumer({'bootstrap.servers': "localhost:9092", 'group.id': sys.argv[1], 'auto.offset.reset': 'latest'})
c.subscribe(["numeric"])

while True:
	msg = c.poll(1.0)

	if msg is None or msg.error():
		continue

	class_data= json.loads((msg.value()).decode('utf-8'))
	# print("****\nstrength= ", class_data['strength'], "seats= ", class_data['seats'], "\n******")
	run_actionNotify(class_data)