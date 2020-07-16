import socket, threading, schedule, json, time ,glob, os, signal, sqlite3
from confluent_kafka import Consumer, KafkaError, Producer
p = Producer({'bootstrap.servers': "localhost:9092"})

def run_logging(username, server_id, server_ip, server_port, app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, pid):
	log_data= {'username' : username,
				'server_id' : server_id,
			   'server_ip' : server_ip,
			   'server_port' : server_port,
			   'app_name': app_name,
			   'service' : service,
			   'freq' : freq,
				'start_time' : start_time,
				'end_time': end_time,
			   'path_app' : path_app,
			   'path_service' : path_service,
			   'algo_name' : algo_name,
			   'pid' : pid
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

def run_server(app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, username, phone_number, email, firstname):
	# Communication with Load Balancer to get appropriate server
	server_id, server_ip, server_port= run_loadBalancer(service, path_app)

	# Communication with Deployer to install the dependencies
	run_deployer(service, path_app, server_id, server_ip, server_port)

	# Communication with Server to execute the service
	rs = socket.socket()  
	rs.connect(('127.0.0.1', int(server_port))) 

	request_data= {
			   'app_name': app_name,
			   'service' : service,
			   'freq' : freq,
				'start_time' : start_time,
				'end_time': end_time,
			   'path_app' : path_app,
			   'path_service' : path_service,
			   'algo_name' : algo_name,
			   'username' : username,
			   'phone_number' :phone_number,
			   'email' : email,
			   'firstname' : firstname,
	}
	request_data= json.dumps(request_data)
	rs.send(bytes(request_data, 'utf-8'))
	pid= rs.recv(1024).decode('utf-8')

	# Communication with Logging to update and store logs
	run_logging(username, server_id, server_ip, server_port, app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, pid)


def kill_service(username, app_name, service, freq, start_time, end_time):
	connection = sqlite3.connect("../Server_DB.sqlite3") 
	crsr = connection.cursor() 
	try:
		task= (username, app_name, service, freq, start_time, end_time)
		sql_command= ''' SELECT pid FROM Logs WHERE username= ? and app_name= ? and service= ? and freq= ? and start_time= ? and end_time= ? '''
		crsr.execute(sql_command, task)
		pid= crsr.fetchall()
		os.kill(pid[0][0], signal.SIGSTOP)
		print ("@@@@@@@@@@@@", pid[0][0], "@@@@@@@@@@@@")
		task= (username, app_name, service, freq, start_time, end_time)
		sql_command= '''DELETE FROM Logs WHERE username= ? and app_name= ? and service= ? and freq= ? and start_time= ? and end_time= ? '''
		crsr.execute(sql_command, task)
		connection.commit()
		print ("Deletion Successful.")
		connection.commit()
	except:
		print ("Failed to delete.")
	
def schedule_algorithm(app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, username, phone_number, email, firstname):

	if (freq == "Sunday"):
		schedule.every().sunday.at(start_time).do(run_server, app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, username, phone_number, email, firstname)
		schedule.every().sunday.at(end_time).do(kill_service, username, app_name, service, freq, start_time, end_time)

	elif (freq == "Monday"):
		schedule.every().monday.at(start_time).do(run_server, app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, username, phone_number, email, firstname)
		schedule.every().monday.at(end_time).do(kill_service, username, app_name, service, freq, start_time, end_time)

	elif (freq == "Tuesday"):
		schedule.every().tuesday.at(start_time).do(run_server, app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, username, phone_number, email, firstname)
		schedule.every().tuesday.at(end_time).do(kill_service, username, app_name, service, freq, start_time, end_time)

	elif (freq == "Wednesday"):
		schedule.every().wednesday.at(start_time).do(run_server, app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, username, phone_number, email, firstname)
		schedule.every().wednesday.at(end_time).do(kill_service, username, app_name, service, freq, start_time, end_time)

	elif (freq == "Thursday"):
		schedule.every().thursday.at(start_time).do(run_server, app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, username, phone_number, email, firstname)
		schedule.every().thursday.at(end_time).do(kill_service, username, app_name, service, freq, start_time, end_time)

	elif (freq == "Friday"):
		schedule.every().friday.at(start_time).do(run_server, app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, username, phone_number, email, firstname)
		schedule.every().friday.at(end_time).do(kill_service, username, app_name, service, freq, start_time, end_time)

	elif (freq == "Saturday"):
		schedule.every().saturday.at(start_time).do(run_server, app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, username, phone_number, email, firstname)
		schedule.every().saturday.at(end_time).do(kill_service, username, app_name, service, freq, start_time, end_time)

	elif (freq == "All"):
		schedule.every().day.at(start_time).do(run_server, app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, username, phone_number, email, firstname)
		schedule.every().day.at(end_time).do(kill_service, username, app_name, service, freq, start_time, end_time)

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

		_request_= json.loads(c.recv(1024).decode("utf-8"))
		c.send(bytes("ack", 'utf-8'))

		# Communication with UI
		app_name= _request_['app_name']
		# print(app_name, type(app_name))

		service= _request_['service']
		# print (service, type(service))

		freq= _request_['freq']
		# print(freq, type(freq))

		start_time= _request_['start_time']
		# print(start_time, type(start_time))

		end_time= _request_['end_time']
		# print(end_time, type(end_time))

		path_app= _request_['path_app']
		# print(path_app, type(path_app))
		
		path_service= _request_['path_service']
		# print(path_service, type(path_service))

		algo_name= _request_['algo_name']
		# print(algo_name, type(algo_name))

		username= _request_['username']
		# print(username, type(username))

		phone_number= _request_['phone_number']
		# print(phone_number, type(phone_number))

		email= _request_['email']
		# print(email, type(email))

		firstname= _request_['firstname']
		# print(firstname, type(firstname))

		
		c.close() 
		
		t= threading.Thread(target=schedule_algorithm, args=(app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, username, phone_number, email, firstname))
		t.start()



