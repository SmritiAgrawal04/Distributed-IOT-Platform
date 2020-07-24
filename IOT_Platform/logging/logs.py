from kafka import KafkaConsumer
import json,sqlite3
from datetime import datetime

print ("LOGGING STARTED")
log_id= 1

def prep_logs(log):
    global log_id
    print ("logs= ",log_data)
    connection = sqlite3.connect("../Server_DB.sqlite3") 
    crsr = connection.cursor()
    try:
        task= (log_id, log['username'], log['server_id'], log['server_ip'], int(log['server_port']), log['app_name'], log['service'], log['freq'], log['start_time'], log['end_time'], log['path_app'], log['path_service'], log['algo_name'], str(datetime.now()), int(log['pid']))
        sql_command= '''INSERT INTO Logs (log_id, username, server_id, server_ip, server_port, app_name, service, freq, start_time, end_time, path_app, path_service, algo_name, datetime, pid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        crsr.execute(sql_command, task)
        connection.commit()
        log_id +=1
        print ("Insertion Done")
        connection.close()
    except:
        print("Insertion Failed")


c = KafkaConsumer('logger' ,bootstrap_servers= "localhost:9092", group_id= '1')
# c.subscribe(['logger'])

for msg in c:

    if msg is None :
        print ("None")
        continue

    log_data= json.loads(msg.value.decode('utf-8'))
    # print (log_data)
    prep_logs(log_data)
        