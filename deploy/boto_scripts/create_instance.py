import boto3
import botocore

def create_instance(pem_key):

	try:
		ec2 = boto3.resource('ec2')
	except botocore.exceptions.ClientError as e:
		print(e)

	try:
		instance = ec2.create_instances(
		#ImageId = 'ami-033b95fb8079dc481',
                # switched it to ubuntu...
                ImageId = 'ami-0e472ba40eb589f49',
		MinCount = 1,
		MaxCount = 1,
		InstanceType = 't2.micro',
		KeyName = pem_key,
		TagSpecifications= [
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                                    {
                                        'Key': 'InstanceKey',
                                        'Value': 'InstanceValue'
                                    },
                                ]
                   },
              	],
		SecurityGroups=['final_project'],
                BlockDeviceMappings=[{"DeviceName": "/dev/sda1","Ebs" : { "VolumeSize" : 10 }}]
		)
		instance_id = instance[0].id
		instance[0].wait_until_running()
		instance[0].load()
		waiter=boto3.client('ec2').get_waiter('instance_status_ok')
		waiter.wait(InstanceIds=[instance_id])
		return instance[0].public_ip_address
	except botocore.exceptions.ClientError as e:
		print(e)

#create_instance()
