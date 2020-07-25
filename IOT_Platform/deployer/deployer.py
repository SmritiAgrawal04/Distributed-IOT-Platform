import socket,os

s = socket.socket()          
port = 8080                
s.bind(('', port))         
s.listen(5) 
print("Deployer Service up and running..")
while True: 

	c, addr = s.accept()  
	# print ("Connection Successful") 

	server_id= c.recv(1024).decode('utf-8')
	c.send(bytes("ack", 'utf-8'))
	server_ip= c.recv(1024).decode('utf-8')
	c.send(bytes("ack", 'utf-8'))
	server_port= int(c.recv(1024).decode('utf-8'))
	c.send(bytes("ack", 'utf-8'))

	num_depend= int(c.recv(1024).decode('utf-8'))
	c.send(bytes("ack", 'utf-8'))
	for num in range (0, num_depend):
		depend= c.recv(1024).decode('utf-8')
		# print(depend, type(depend))
		install = socket.socket()  
		install.connect(('127.0.0.1', int(server_port)+1)) 
		install.send(bytes(depend, 'utf-8'))
		install.recv(1024)
		c.send(bytes("ack", 'utf-8'))
	c.close()