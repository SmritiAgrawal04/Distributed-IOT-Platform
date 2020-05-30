from datetime import datetime
myFile = open('appenduser2.txt', 'a') 
myFile.write('\nAccessed on ' + str(datetime.now())+ '\nI am user 2')
