from confluent_kafka import Consumer, KafkaError, Producer
import json, threading, socket
from server_data import *
statistics = {}
s = socket.socket()          
port = 1234              
s.bind(('', port))         
s.listen(5)      

def get_stats():
	c = Consumer({'bootstrap.servers': "localhost:9092", 'group.id': '1', 'auto.offset.reset': 'latest'})
	c.subscribe(['load_balancer'])

	while True:
		msg = c.poll(1.0)

		if msg is None or msg.error():
			continue

		statistics= json.loads(msg.value().decode('utf-8'))
		# print(statistics)   
		prep_serverInfo(statistics)

def respond_scheduler():
	while True:
		c, addr = s.accept() 
		print ("Connection Successful to respond to Scheduler")
		cpu_requirement= float(c.recv(1024).decode('utf-8'))
		c.send(bytes("ack", 'utf-8'))
		memory_requirement= float(c.recv(1024).decode('utf-8'))
		server= get_server(cpu_requirement, memory_requirement)
		c.send(bytes(str(server[0]), 'utf-8'))
		c.close()
		

if __name__ == "__main__":
	
	t_stats= threading.Thread(target= get_stats)
	t_stats.start()

	t_sched= threading.Thread(target= respond_scheduler)
	t_sched.start()
	