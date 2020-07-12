from confluent_kafka import Producer
import psutil, json, time, socket, threading, os, shutil

server_id= 'server3'
server_port= 7004

def installDependencies():
	install = socket.socket()
	port = 7005              
	install.bind(('', port))         
	install.listen(5) 

	while True: 
		c, addr = install.accept()
		print ("Deployer Connected to Server")
		depend= c.recv(1024).decode('utf-8')
		c.send(bytes("ack", 'utf-8'))
		os.system(depend)

p = Producer({'bootstrap.servers': "localhost:9092"})
def sendStats():
	while True:
		hostname = socket.gethostname()
		server_ip= socket.gethostbyname(hostname) 
		# print (server_ip)

		cpu_utilization= psutil.cpu_percent()
		# print (cpu_utilization)

		total_memory= psutil.virtual_memory().total
		# print (total_memory)

		used_memory= psutil.virtual_memory().used/total_memory *100
		# print (used_memory)

		free_memory= psutil.virtual_memory().available/total_memory *100
		# print (free_memory)


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


def startAction(request_data):
	app_name= request_data['app_name']
	service= request_data['service']
	period= request_data['period']
	freq= request_data['freq']
	path_app= request_data['path_app']
	path_service= request_data['path_service']
	algo_name= request_data['algo_name']
	username= request_data['username']
	email= request_data['email']
	firstname= request_data['firstname']
	lastname= request_data['lastname']

	# exec(open(path+algo_name).read())
	shutil.copyfile(path_service+algo_name, "./{}".format(algo_name))
	command="python3 {} {} '{}' '{}' '{}' '{}' '{}' '{}'".format(algo_name, 3, app_name, service, username, email, firstname, lastname)
	print("command= ", command)
	os.system(command)
	


def runService():
	s = socket.socket()          
	port = 7004             
	s.bind(('', port))         
	s.listen(5) 

	while True: 
		c, addr = s.accept()
		print ("Connection Established")
		request_data= json.loads(c.recv(1024).decode('utf-8'))
		c.send(bytes("ack", 'utf-8'))

		print ("Ready to Schedule the Algorithm")
		t_action= threading.Thread(target=startAction, args= (request_data, ))
		t_action.start()
		

if __name__ == "__main__":
	t_sendStats= threading.Thread(target=sendStats)
	t_runService= threading.Thread(target=runService)
	t_installDependencies= threading.Thread(target=installDependencies)

	t_sendStats.start()
	t_runService.start()
	t_installDependencies.start()