from confluent_kafka import Consumer, KafkaError
from datetime import datetime
import json,sqlite3
from email_notif import email_notification
from message_notif import message_notification
from alarm_notif import alarm_notification
print("Notification Manager Service up and running..")

c = Consumer({'bootstrap.servers': "localhost:9092", 'group.id': '1', 'auto.offset.reset': 'latest'})
c.subscribe(['notify'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        continue
    
    # print('Received message: {}'.format(msg.value().decode('utf-8')))
    _request_= json.loads(msg.value().decode('utf-8'))
    connection = sqlite3.connect("db.sqlite3") 
    crsr = connection.cursor() 
    try:
        task= (_request_['username'], _request_['phone_number'], _request_['email'], _request_['firstname'], _request_['app_name'], _request_['service'], str(datetime.now()), _request_['message'], _request_['notify_type'])
        sql_command = '''INSERT INTO action_notification_notifications (username, phone_number, email, firstname, app_name, service, datetime, message, notify_type) VALUES (?,?,?,?,?,?,?,?,?)'''
        crsr.execute(sql_command, task)
        connection.commit()
        # print ("Insertion Done")

        try:
            noti_types= _request_['notify_type'].split(",")
            if 'email' in noti_types:
                email_notification(_request_)
            if 'message' in noti_types:
                message_notification(_request_)
            if 'alarm' in noti_types:
                alarm_notification(_request_)
            # print ("Notification Sent from try")
        except:
            if _request_['notify_type'] == 'email':
                email_notification(_request_)
            if _request_['notify_type'] == 'message':
                message_notification(_request_)
            if _request_['notify_type'] == 'alarm':
                alarm_notification(_request_)
            # print ("Notification Sent from except")

    except:
        # print ("Insertion Failed")
        continue

        