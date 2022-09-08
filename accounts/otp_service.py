
from twilio.rest import Client 
import random


def generate_opt():
    n=random.randrange(1000,9999)
    return n

customer_number = '+917011101001'

def send_otp(customer_number,current_otp):
    #Messaging Service created and phone number provisioned. Your Messaging Service SID is MG550b81ea293631fa1af1f178be912b6f
    account_sid = 'AC2affb3fcd424dbfa4a44940a42ef5b9b'
    auth_token = 'd3e0847eefff6dce5ddf23639c45c2e0'
    client = Client(account_sid, auth_token)
    # current_otp=otp
    customer_number_='+91'+str(customer_number)
    message = client.messages.create(
        body=' is your MySchool OTP.\nDo not share it with anyone.',
        messaging_service_sid='MG550b81ea293631fa1af1f178be912b6f',
        to=customer_number)
    return




# account_sid = 'AC2affb3fcd424dbfa4a44940a42ef5b9b' 
# auth_token = 'd3e0847eefff6dce5ddf23639c45c2e0' 
# client = Client(account_sid, auth_token) 
 
# message = client.messages.create(  
#                               messaging_service_sid='MG550b81ea293631fa1af1f178be912b6f', 
#                               body='hello',      
#                               to='+917011101001' 
#                           ) 
 
# print(message.sid)       



