import socket,os

s = socket.socket()          
port = 8080                
s.bind(('', port))         
s.listen(5) 

while True: 

    c, addr = s.accept()  
    print ("Connection Successful") 
    num_depend= int(c.recv(1024).decode('utf-8'))
    c.send(bytes("ack", 'utf-8'))
    for num in range (0, num_depend):
        depend= c.recv(1024).decode('utf-8')
        print(depend, type(depend))
        os.system(depend)
        c.send(bytes("ack", 'utf-8'))
    c.close()