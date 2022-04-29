import boto3
import botocore

def get_vpc_info():
    
    try:
        client = boto3.client('ec2')
        response = client.describe_vpcs()
        return response
        
    except botocore.exceptions.ClientError as e:
        print(e)
        pass

def main():

    print(get_vpc_info().get('Vpcs')[0].get('VpcId'))

if __name__ == "__main__":
    main()