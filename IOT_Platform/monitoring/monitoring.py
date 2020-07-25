from confluent_kafka import Consumer, KafkaError, Producer
import json,time
statistics= {}
p = Producer({'bootstrap.servers': "localhost:9092"})
print("Monitoring Service up and running..")

def inform_loadBalancer():
	json_string= json.dumps(statistics)
	p.produce('load_balancer', json_string.encode('utf-8'))
	p.poll(0)
	time.sleep(10)

def update_statistics(stats):
	key= json.loads(stats)['server_id']
	statistics[key]= json.loads(stats)
	inform_loadBalancer()

if __name__ == "__main__":
	
	c = Consumer({'bootstrap.servers': "localhost:9092", 'group.id': '1', 'auto.offset.reset': 'latest'})
	c.subscribe(['server_stats'])

	while True:
		msg = c.poll(1.0)

		if msg is None or msg.error():
			continue

		# print (statistics)
		# print("****")
		update_statistics(msg.value().decode('utf-8'))   
	