import boto3
import botocore

def create_instance(pem_key, min_num_of_instances, max_num_of_instances):

    try:
        ec2 = boto3.resource('ec2')
    except botocore.exceptions.ClientError as e:
        print(e)

    try:
        instance = ec2.create_instances(
        #ImageId = 'ami-033b95fb8079dc481',
                # switched it to ubuntu...
                ImageId = 'ami-0e472ba40eb589f49',
        MinCount = min_num_of_instances,
        MaxCount = max_num_of_instances,
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

        ip_addresses = []
        for instance_num in range(max_num_of_instances):
            try:
                instance_id = instance[instance_num].id
                print('please wait while instance is being created..')
                instance[instance_num].wait_until_running()
                instance[instance_num].load()
                waiter = boto3.client('ec2').get_waiter('instance_status_ok')
                waiter.wait(InstanceIds=[instance_id])
                print('instance is ready')
                ip_addresses.append(instance[instance_num].public_ip_address)
            except:
                continue
        return ip_addresses

    except botocore.exceptions.ClientError as e:
        print(e)

#create_instance()
