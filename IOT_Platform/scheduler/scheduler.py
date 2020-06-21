import socket, threading, schedule, json, time ,glob  
from confluent_kafka import Consumer, KafkaError, Producer
p = Producer({'bootstrap.servers': "localhost:9092"})

def run_logging(server_id, server_ip, server_port, app_name, service, period, freq, path_app, path_service, algo_name):
	log_data= {'server_id' : server_id,
			   'server_ip' : server_ip,
			   'server_port' : server_port,
			   'app_name': app_name,
			   'service' : service,
			   'period' : period,
			   'freq' : freq,
			   'path_app' : path_app,
			   'path_service' : path_service,
			   'algo_name' : algo_name
	}
	log_data= json.dumps(log_data)
	p.produce('logger', log_data.encode('utf-8'))
	p.poll(0)

def run_deployer(service, path_app, server_id, server_ip, server_port):
	dep = socket.socket()  
	dep.connect(('127.0.0.1', int(8080))) 

	for file in glob.glob(path_app):
		f= open(file)
		result= f.read()
		json_result= json.loads(result)
	entry= json_result[service]
	dependencies= entry['dependencies']
	print (dependencies, len(dependencies))

	dep.send(bytes(server_id, 'utf-8'))
	dep.recv(1024)
	dep.send(bytes(server_ip, 'utf-8'))
	dep.recv(1024)
	dep.send(bytes(str(server_port), 'utf-8'))
	dep.recv(1024)

	dep.send(bytes(str(len(dependencies)),'utf-8'))
	dep.recv(1024)
	for num_depend in range (0, len(dependencies)):
		dep.send(bytes(dependencies[num_depend], 'utf-8'))
		dep.recv(1024)

def run_loadBalancer(service, path_app):
	lb = socket.socket()  
	port = 1234
	lb.connect(('127.0.0.1', port)) 

	for file in glob.glob(path_app):
		f= open(file)
		result= f.read()
		json_result= json.loads(result)
	entry= json_result[service]
	cpu_requirement= entry['cpu_requirement']
	memory_requirement= entry['memory_requirement']

	lb.send(bytes(str(cpu_requirement), 'utf-8'))
	lb.recv(1024)
	lb.send(bytes(str(memory_requirement), 'utf-8'))
	server= lb.recv(1024).decode('utf-8')
	server_id= (server.split(',')[0]).split('(')[1]
	server_ip= server.split(',')[1]
	server_port= server.split(',')[2]
	print (server_id, server_ip, server_port)
	return server_id, server_ip, server_port

def run_server(app_name, service, period, freq, path_app, path_service, algo_name):
	# Communication with Load Balancer to get appropriate server
	server_id, server_ip, server_port= run_loadBalancer(service, path_app)

	# Communication with Deployer to install the dependencies
	run_deployer(service, path_app, server_id, server_ip, server_port)

	# Communication with Logging to update ans store logs
	run_logging(server_id, server_ip, server_port, app_name, service, period, freq, path_app, path_service, algo_name)

	# Communication with Server to execute the service
	rs = socket.socket()  
	rs.connect(('127.0.0.1', int(server_port))) 

	request_data= {
			   'app_name': app_name,
			   'service' : service,
			   'period' : period,
			   'freq' : freq,
			   'path_app' : path_app,
			   'path_service' : path_service,
			   'algo_name' : algo_name
	}
	request_data= json.dumps(request_data)
	rs.send(bytes(request_data, 'utf-8'))
	rs.recv(1024)


def schedule_algorithm(app_name, service, period, freq, path_app, path_service, algo_name):
	if period== "Weekly":

		if (freq == "Sunday"):
			schedule.every().sunday.do(run_server)
		if (freq == "Monday"):
			schedule.every().monday.do(run_server)
		if (freq == "Tuesday"):
			schedule.every().tuesday.do(run_server)
		if (freq == "Wednesday"):
			schedule.every().wednesday.do(run_server)
		if (freq == "Thursday"):
			schedule.every().thursday.do(run_server)
		if (freq == "Friday"):
			schedule.every().friday.do(run_server)
		if (freq == "Saturday"):
			schedule.every().saturday.do(run_server)

	elif period== "Hourly":
		schedule.every(freq).hour.do(run_server)

	elif period== "Minutely":
		schedule.every(freq).minutes.do(run_server, app_name, service, period, freq, path_app, path_service, algo_name)

	while True: 
		schedule.run_pending() 
		time.sleep(1)
  
if __name__ == "__main__":

	s = socket.socket()          
	port = 12345                
	s.bind(('', port))         
	s.listen(5) 

	while True: 
	
		c, addr = s.accept()      
		
		# Communication with UI
		app_name= c.recv(1024).decode("utf-8")
		print(app_name, type(app_name))
		c.send(bytes("ack", 'utf-8'))

		service= c.recv(1024).decode("utf-8")
		print (service, type(service))
		c.send(bytes("ack", 'utf-8'))

		period= c.recv(1024).decode("utf-8")
		print(period, type(period))
		c.send(bytes("ack", 'utf-8'))

		freq= c.recv(1024).decode("utf-8")
		if period != "Weekly":
			freq= float(freq)    
		print(freq, type(freq))
		c.send(bytes("ack", 'utf-8'))

		path_app= c.recv(1024).decode("utf-8")
		print(path_app, type(path_app))
		c.send(bytes("ack", 'utf-8'))
		
		path_service= c.recv(1024).decode("utf-8")
		print(path_service, type(path_service))
		c.send(bytes("ack", 'utf-8'))

		algo_name= c.recv(1024).decode("utf-8")
		print(algo_name, type(algo_name))
		c.send(bytes("ack", 'utf-8'))
		
		c.close() 
		
		t= threading.Thread(target=schedule_algorithm, args=(app_name, service, period, freq, path_app, path_service, algo_name))
		t.start()



