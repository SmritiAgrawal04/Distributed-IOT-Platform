# importing twilio 
from twilio.rest import Client 
  
# Your Account Sid and Auth Token from twilio.com / console 
account_sid = 'AC65bd55c27c4404768d9a78b1bcaa354d'
auth_token = 'ff00702442f2e151e67c11cafe0ebb99'
  
client = Client(account_sid, auth_token) 
  
''' Change the value of 'from' with the number  
received from Twilio and the value of 'to' 
with the number in which you want to send message.'''
message = client.messages.create( 
                              from_='+13343848206', 
                              body ='Hello bc!', 
                              to ='8989648989'
                          ) 
  
print(message.sid) 