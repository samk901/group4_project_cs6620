import boto3
import botocore


def create_instance(pem_key, num_instances=1):
    try:
        ec2 = boto3.resource('ec2')
    except botocore.exceptions.ClientError as e:
        print(e)

    try:
        instances = ec2.create_instances(
            #  Ubuntu 18.04 LTS
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
            BlockDeviceMappings=[
                {"DeviceName": "/dev/sda1", "Ebs": {"VolumeSize": 10}}]
        )
        print('please wait while {num} instances are being created..'.format(
            num=num_instances))

        # ip_addresses = []
        for num in range(num_instances):
            try:
                instance_id = instances[num].id
                instances[num].wait_until_running()
                instances[num].load()
                waiter = boto3.client('ec2').get_waiter('instance_status_ok')
                waiter.wait(InstanceIds=[instance_id])
                print('instance {ip} is ready'.format(
                    ip=instances[num].public_ip_address))
                # ip_addresses.append(instances[instance_num].public_ip_address)
            except Exception as e:
                print(e)
        # return ip_addresses
        return instances

    except botocore.exceptions.ClientError as e:
        print(e)
