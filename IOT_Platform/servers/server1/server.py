from confluent_kafka import Producer
import psutil, json, time, socket, threading

server_id= 'server1'
server_port= 7000

p = Producer({'bootstrap.servers': "localhost:9092"})

def sendStats():
	while True:
		hostname = socket.gethostname()
		server_ip= socket.gethostbyname(hostname) 
		print (server_ip)

		cpu_utilization= psutil.cpu_percent()
		print (cpu_utilization)

		total_memory= psutil.virtual_memory().total
		print (total_memory)

		used_memory= psutil.virtual_memory().used/total_memory *100
		print (used_memory)

		free_memory= psutil.virtual_memory().available/total_memory *100
		print (free_memory)


		stats= {
			"server_id" : server_id,
			"server_ip" : server_ip,
			"server_port": server_port,
			"cpu_utilization" : cpu_utilization,
			"used_memory" : used_memory,
			"free_memory" : free_memory
		}

		json_string= json.dumps(stats)
		p.produce('server_stats', json_string.encode('utf-8'))
		p.poll(0)

		time.sleep(10)

def runService():
	s = socket.socket()          
	port = 7000                
	s.bind(('', port))         
	s.listen(5) 

	while True: 
		c, addr = s.accept()
		print ("Connection Established")
		path= c.recv(1024).decode('utf-8')
		c.send(bytes("ack", 'utf-8'))
		algo_name= c.recv(1024).decode('utf-8')
		c.send(bytes("ack", 'utf-8'))

		print ("Ready to Schedule the Algorithm")
		exec(open(path+algo_name).read())

if __name__ == "__main__":
	t_sendStats= threading.Thread(target=sendStats)
	t_runService= threading.Thread(target=runService)

	t_sendStats.start()
	t_runService.start()