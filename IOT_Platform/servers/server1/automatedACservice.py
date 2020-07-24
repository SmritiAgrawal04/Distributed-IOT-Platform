from kafka import KafkaProducer, KafkaConsumer
import time, sys, json, socket, os
from datetime import datetime

p = KafkaProducer(bootstrap_servers= "localhost:9092")

def run_actionNotify(value):
	if value>=10 and value<=59:
		message= "Your {} at {} had a LOW TEMPERATURE of {} in {}".format(sys.argv[3], str(datetime.now()), str(value), sys.argv[7])
	elif value>=60 and value<=100:
		message= "Your {} at {} had a NORMAL TEMPERATURE of {} in {}".format(sys.argv[3], str(datetime.now()), str(value), sys.argv[7])
	elif value>=101 and value<+120:
		message= "Your {} at {} had a HIGH TEMPERATURE of {} in {}".format(sys.argv[3], str(datetime.now()), str(value), sys.argv[7])
	else:
		return

	notify_data= {'notify_type': "",
				  'app_name' : sys.argv[2],
				  'service' : sys.argv[3],
				  'username' : sys.argv[4],
				  'phone_number' : sys.argv[5],
				  'email' : sys.argv[6],
				  'firstname' : sys.argv[7],
				  'message' : message
	}

	notify_data= json.dumps(notify_data)
	p.send('notify', notify_data.encode('utf-8'))


c = KafkaConsumer(bootstrap_servers= "localhost:9092", group_id= sys.argv[1])
c.subscribe(["temp_ac"])
print ("************************************in service", os.getpid(), "*******************************************")
for msg in c:

	if msg is None:
		continue

	# print ("####", sys.argv[2], sys.argv[3],sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
	value= int((msg.value).decode('utf-8'))
	# print("****value= ", value, "******")
	run_actionNotify(value)