from confluent_kafka import Consumer, KafkaError, Producer
import json,sqlite3
from datetime import datetime

log_id= 1

def prep_logs(log):
    global log_id
    print ("logs= ",log_data)
    connection = sqlite3.connect("../Server_DB.sqlite3") 
    crsr = connection.cursor() 
 
    try:
        task= (log_id, log['server_id'], log['server_ip'], int(log['server_port']), log['app_name'], log['service'], log['period'], log['freq'], log['path_app'], log['path_service'], log['algo_name'], str(datetime.now()))
        sql_command= '''INSERT INTO Logs (log_id, server_id, server_ip, server_port, app_name, service, period, freq, path_app, path_service, algo_name, datetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        crsr.execute(sql_command, task)
        connection.commit()
        log_id +=1
        print ("Insertion Done")
    except:
        print("Insertion Failed")
    
        
c = Consumer({'bootstrap.servers': "localhost:9092", 'group.id': '1', 'auto.offset.reset': 'latest'})
c.subscribe(['logger'])

while True:
    msg = c.poll(1.0)

    if msg is None or msg.error():
        continue

    log_data= json.loads(msg.value().decode('utf-8'))
    # print (log_data)
    prep_logs(log_data)
    