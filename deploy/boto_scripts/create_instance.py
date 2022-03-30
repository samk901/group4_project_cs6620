import boto3
import botocore

def create_instance():

	try:
		ec2 = boto3.resource('ec2')
	except botocore.exceptions.ClientError as e:
		print(e)

	try:
		instance = ec2.create_instances(
		ImageId = 'ami-033b95fb8079dc481',
		MinCoint = 1,
		MaxCount = 1,
		InstanceType = 't2.micro',
		KeyName = 'lab2key',
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
		BlockDeviceMappings=[{"DeviceName": "/dev/xvda","Ebs" : { "VolumeSize" : 10 }}]
		)
	except: boto3core.exceptions.ClientError as e:
		print(e)

create_instance()
