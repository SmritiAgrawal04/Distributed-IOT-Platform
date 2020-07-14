from twilio.rest import Client 

def message_notification(_request_):
    print ("$$$$$$$$In message Notification$$$$$$$$")
    account_sid = 'AC65bd55c27c4404768d9a78b1bcaa354d'
    auth_token = 'ff00702442f2e151e67c11cafe0ebb99'
    phone_number= "+91"+ _request_['phone_number']
    client = Client(account_sid, auth_token) 
    
    ''' Change the value of 'from' with the number  
    received from Twilio and the value of 'to' 
    with the number in which you want to send message.'''
    message = client.messages.create( 
                                from_='+13343848206', 
                                body = "Hi {},\nThe current status of your service {} of {} is {}.".format(_request_['firstname'], _request_['service'], _request_['app_name'], _request_["value"]), 
                                to = phone_number
                            ) 
    
    print(message.sid) 