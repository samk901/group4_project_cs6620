import boto3

def create_pem():
    try:
        ec2 = boto3.client('ec2')
        keyname = 'final_project_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=))
        response = ec2.create_key_pair(KeyName=keyname)
        #print(response.keys())
        with open('./'+keyname+'.pem', 'w') as file:
            file.write(response.get('KeyMaterial'))
        return keyname + '.pem'
    except:
        print('Error creating key')

