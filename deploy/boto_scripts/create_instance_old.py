import boto3
import botocore


def create_instance(pem_key, num_instances=1):
    try:
        ec2 = boto3.resource('ec2')
    except botocore.exceptions.ClientError as e:
        print(e)

    try:
        instances = ec2.create_instances(

            ImageId='ami-0e472ba40eb589f49',
            MinCount=num_instances,
            MaxCount=num_instances,
            InstanceType='t2.micro',
            KeyName=pem_key,
            TagSpecifications=[
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
            BlockDeviceMappings=[{"DeviceName": "/dev/sda1", "Ebs": {"VolumeSize": 10}}]
        )
        ids = [i.id for i in instances]
        print('please wait while instance is being created..')

        waiter = boto3.client('ec2').get_waiter('instance_status_ok')
        waiter.wait(InstanceIds=ids)
        print('instances are ready')
        ips = [i.public_ip_address for i in instances]
        return ips
    except botocore.exceptions.ClientError as e:
        print(e)
