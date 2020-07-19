from confluent_kafka import Consumer, KafkaError, Producer
import time, sys, json, os

p = Producer({'bootstrap.servers': "localhost:9092"})

def run_actionNotify(value):
	if value ==0:
		return
	else:
		message= "Hi {},\nSomeone might be accesing the {} illegaly. Please Check!".format(sys.argv[7], sys.argv[8])
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
c.subscribe(["binary"])
print ("************************************in service", os.getpid(), "*******************************************")


while True:
	msg = c.poll(1.0)

	if msg is None or msg.error():
		continue

	value= int((msg.value()).decode('utf-8'))
	print("****value= ", value, "******")
	run_actionNotify(value)