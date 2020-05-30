# Python program to demonstrate 
# creating a new file 
  
  
# importing module 
import os 
  
# path of the current script 
path = './'
  
# Before creating 
# dir_list = os.listdir(path)  
# print("List of directories and files before creation:") 
# print(dir_list) 
# print() 
  
# Creates a new file 
with open(path+ 'myfileuser2.txt', 'w') as fp: 
    fp.write("New file created") 
	# pass
	# To write data to new file uncomment 
	
  
# After creating  
# dir_list = os.listdir(path) 
# print("List of directories and files after creation:") 
# print(dir_list)