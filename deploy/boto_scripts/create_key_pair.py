import boto3

def create_pem():
    ec2 = boto3.client('ec2')
    response = ec2.create_key_pair(KeyName='final_project_key')
    #print(response.keys())
    with open('./final_project_key.pem', 'w') as file:
        file.write(response.get('KeyMaterial'))

