import boto3
import botocore

def get_vpc_info():
    
    try:
        client = boto3.client('ec2')
        response = client.describe_vpcs()
        return response.get('Vpcs')[0].get('VpcId')
        
    except botocore.exceptions.ClientError as e:
        print(e)
        pass

def get_subnets():
    
    try:
        client = boto3.client('ec2')
        response = client.describe_subnets()
        return [response.get('Subnets')[0].get('SubnetId'), response.get('Subnets')[1].get('SubnetId')]
        
    except botocore.exceptions.ClientError as e:
        print(e)
        pass