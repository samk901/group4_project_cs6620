""""
Samuel D. Kim
CS6620, Lab2: EC2

This script will create an EC2 instance on the specified VPC with the appropriate security groups.
This program assumes a clean environment (e.g. no pem file, no pre-existing security group), but will use the
pre-existing vpc. It can also create a default vpc, but the user will need to update the global vpc info at the top 
of the file. 
"""

import boto3
import logging
from botocore.exceptions import ClientError
import json
import os

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

AWS_REGION = "us-east-2"
AMI_ID = "ami-0b614a5d911900a9b"
vpc_client = boto3.client("ec2", region_name=AWS_REGION)
get_vpc_response = vpc_client.describe_vpcs()
vpc_id = get_vpc_response.get("Vpcs", [{}])[0].get("VpcId", "")


def create_ec2_key_pair():
    """
    This function will instantiate a client, delete the existing pair with KeyName='Name'.
    Then it will create a key pair, store the private key in my_key.pem to current working directory.
    """
    ec2_client = boto3.client("ec2", region_name=AWS_REGION)

    # Block used for testing, deletes key_pair
    try:

        ec2_client.delete_key_pair(KeyName="Name")
        response = ec2_client.describe_key_pairs()
        logger.info(
            "Key_Pair with KeyName: 'Name' has been deleted in vpc " + vpc_id)

    except ClientError as e:
        logger(e)

    try:
        key_pair = ec2_client.create_key_pair(
            KeyName="Name",
            TagSpecifications=[
                {
                    "ResourceType": "key-pair",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "cs6620-ec2-lab2",
                        },
                    ],
                }
            ]
        )

        logger.info("Created 'Name' key_pair")

        private_key = key_pair["KeyMaterial"]

        with open("./my_key1.pem", "w+") as file:
            file.write(private_key)

        logger.info("Saved private key to local system as my_key.pem")

    except ClientError as e:
        logger.error(e)
        logger.error("Failed to create key pair.")

    except IOError as ioe:
        logger.error(ioe)


def create_ec2_instance():
    """
    This function will create a security group, and create and execute a new
    ec2 instance on the VPC with the specified requirements. 
    """
    ec2_client = boto3.client("ec2", region_name=AWS_REGION)

    # Get security group id
    sg_id = create_security_group()

    try:
        response = ec2_client.run_instances(
            BlockDeviceMappings=[
                {
                    "DeviceName": "/dev/xvda",
                    "Ebs": {
                        "VolumeSize": 10
                    },
                }
            ],
            ImageId=AMI_ID,
            InstanceType="t3.nano",
            KeyName="Name",
            MaxCount=1,
            MinCount=1,
            SecurityGroupIds=[sg_id],
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "cs6620-ec2-lab2",
                        },
                    ],
                }
            ]
        )

    except ClientError as e:
        logger.exception(e)

    instance_id = response["Instances"][0]["InstanceId"]
    logger.info("Running instance ID:{} on vpc {}".format(instance_id, vpc_id))

    return response


def create_security_group():
    """
    This function will create a new security group that will allow inbound 
    traffic to our ec2 instance from my IP address and also allow all http traffic
    on port 80.
    """

    ec2_client = boto3.client("ec2", region_name=AWS_REGION)

    # Deletes existing security group if it exists.
    try:
        ec2_client.delete_security_group(GroupName="security")
        logger.info("Security Group Deleted: 'security' in vpc " + vpc_id)

    except ClientError as e:
        logger.exception(e)

    try:
        response = ec2_client.create_security_group(
            Description="Security group for Lab:EC",
            GroupName="security",
            VpcId=vpc_id
        )

        security_group_id = response['GroupId']
        logger.info("Security Group Created %s in vpc %s" %
                    (security_group_id, vpc_id))

        ec2_resource = boto3.resource("ec2")

        # Create security group ingress rules.
        security_group = ec2_resource.SecurityGroup(security_group_id)
        response = security_group.authorize_ingress(
            GroupName="security",
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": 22,
                    "ToPort": 22,
                    "IpRanges": [{"CidrIp": "162.229.177.50/32"}]
                },
                {
                    "IpProtocol": "tcp",
                    "FromPort": 80,
                    "ToPort": 80,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
                }
            ]
        )

    except ClientError as e:
        logger.exception(e)

    return security_group_id


def create_default_vpc():
    """
    This function will create a default vpc instance. 
    """

    try:
        response = vpc_client.create_default_vpc()

    except ClientError:
        logger.exception("Could not create default vpc")
        raise
    else:
        return response


def delete_vpc(vpc_id):
    """
    This function will delete the specified vpc instance. 
    """
    try:
        response = vpc_client.delete_vpc(VpcID=vpc_id)

    except ClientError:
        logger.exception("Could not delete the vpc")
        raise
    else:
        return response


# This is the entry point for our program.
if __name__ == "__main__":

    # The block below can be uncommented to generate the VPC.
    # Then it will overwrite the global variable for the vpc_id.
    """
    logger.info(f'Creating default VPC...')
    default_vpc = create_default_vpc()
    default_vpc_id = default_vpc['Vpc']['VpcId']
    logger.info(f'Default VPC is created with VPD ID: {default_vpc_id}')
    vpc_id = default_vpc_id
    """

    create_ec2_key_pair()

    ec2_create_response = create_ec2_instance()
    ec2_instance_id = ec2_create_response["Instances"][0]["InstanceId"]
    ec2_private_ip = ec2_create_response["Instances"][0]["PrivateIpAddress"]
    ec2_private_dns = ec2_create_response["Instances"][0]["PrivateDnsName"]

    logger.info("ec2 instance launched. Instance Id: " + ec2_instance_id)
    logger.info("Private IP address is : " + ec2_private_ip)
    logger.info("Private DNS Name is : " + ec2_private_dns)
