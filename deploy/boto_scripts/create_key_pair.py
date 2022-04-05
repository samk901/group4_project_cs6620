import boto3
import random
import string

def create_pem():
    ec2 = boto3.client('ec2')
    keyname = 'final_project_' + ''.join(random.choices(string.ascii_uppercase, k=6))
    response = ec2.create_key_pair(KeyName=keyname)
    #print(response.keys())
    with open('./'+keyname+'.pem', 'w') as file:
        file.write(response.get('KeyMaterial'))
    return keyname+ '.pem'
create_pem()

