	# Python code to demonstrate SQL to fetch data. 
  
# importing the module 
import sqlite3 
  
# connect withe the myTable database 
connection = sqlite3.connect("Server_DB.sqlite3") 
  
# cursor object 
crsr = connection.cursor() 

# SQL command to create a table in the database 
sql_command = """CREATE TABLE server_info (  
server_id VARCHAR(20) PRIMARY KEY,  
server_ip VARCHAR(20), 
server_port INTEGER, 
cpu_utilization INTEGER,  
used_memory REAL,
free_memory REAL);"""
  	
# execute the statement 
crsr.execute(sql_command) 
  
# # SQL command to insert the data in the table 
# sql_command = """INSERT INTO server_info VALUES (1, "127.0.0.1", 9090, "1_9090");"""
# crsr.execute(sql_command) 
  
# # another SQL command to insert the data in the table 
# sql_command = """INSERT INTO server_info VALUES (2, "127.0.0.1", 9092, "2_9092");"""
# crsr.execute(sql_command) 
  
# # To save the changes in the files. Never skip this.  
# # If we skip this, nothing will be saved in the database. 
# connection.commit() 
  
# # execute the command to fetch all the data from the table emp 
# crsr.execute("SELECT * FROM server_info")  
  
# # store all the fetched data in the ans variable 
# ans = crsr.fetchall()  
  
# # Since we have already selected all the data entries  
# # using the "SELECT *" SQL command and stored them in  
# # the ans variable, all we need to do now is to print  
# # out the ans variable 
# print(ans) 