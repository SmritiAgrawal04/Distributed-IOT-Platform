from twilio.rest import Client 

def message_notification(_request_):
    print ("$$$$$$$$In message Notification$$$$$$$$")
    account_sid = 'XXXXXXXXXX'
    auth_token = 'XXXXXXXXXXXXXXXXXX'
    phone_number= "+91"+ _request_['phone_number']
    client = Client(account_sid, auth_token) 
    
    ''' Change the value of 'from' with the number  
    received from Twilio and the value of 'to' 
    with the number in which you want to send message.'''
    message = client.messages.create( 
                                from_='+13343848206', 
                                body = 'Hi {},\n{}'.format(_request_['firstname'], _request_['message']),
                                to = phone_number
                            ) 
    
    print(message.sid) 