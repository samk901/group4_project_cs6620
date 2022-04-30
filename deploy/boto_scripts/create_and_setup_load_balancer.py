#Used https://www.youtube.com/watch?v=OGEZn50iUtE as a reference which describes how to manually create load balancer from AWS console

import boto3
import botocore

lb_client = boto3.client('elbv2')

def create_load_balancer_security_group(vpc_id):
    
    try:
        ec2_client = boto3.resource('ec2')
        sg = ec2_client.create_security_group(GroupName="LoadBalancerSG", Description='Security Group for Load Balancer', VpcId=vpc_id,  TagSpecifications=[
                                                                                                        {'ResourceType': 'security-group',
                                                                                                         'Tags': [{'Key': 'LbSgTagKey', 'Value': 'LbSgTagVal'}]
                                                                                                        }
                                                                                                          ])
        sg.authorize_ingress(IpPermissions=[{'IpProtocol': 'TCP',
                                            'FromPort': 3000,
                                            'ToPort': 3000,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            }
                                            ]

                                )
    except botocore.exceptions.ClientError as e:
        print("Create load balancer security group error: " + e)
    else:
        return sg

def create_load_balancer(lb_security_group_id, lb_subnets, lb_name):

    try:
        lb_client = boto3.client('elbv2')

        lb = lb_client.create_load_balancer(
            Name=lb_name,
            Scheme='internet-facing',
            SecurityGroups=[lb_security_group_id
            ],
            Subnets=lb_subnets,
            Type='application',

        )
    except botocore.exceptions.ClientError as e:
        print(e)
    else:
        return lb

def create_target_group(vpc_id, tg_name):

    try:
        lb_client = boto3.client('elbv2')

        tg = lb_client.create_target_group(
            Name=tg_name,
            Port=3000,
            Protocol='HTTP',
            VpcId=vpc_id,
            TargetType='instance'
        )

    except botocore.exceptions.ClientError as e:
        print(e)
    else:
        return tg

#Can call this method for each ec2 instance we have
def register_ec2_instance_with_target_group(target_group_arn, ec2_instance_id):

    try:
        lb_client = boto3.client('elbv2')

        response = lb_client.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=[
                {
                    'Id': ec2_instance_id,
                    'Port': 3000,
                }
            ],
        )

    except botocore.exceptions.ClientError as e:
        print(e)
    else:
        return response

def create_listener(target_group_arn, load_balancer_arn):

    try:
        lb_client = boto3.client('elbv2')

        response = lb_client.create_listener(
            DefaultActions=[
                {
                    'TargetGroupArn': target_group_arn,
                    'Type': 'forward',
                },
                ],
            LoadBalancerArn=load_balancer_arn,
            Port=3000,
            Protocol='HTTP',
        )

    except botocore.exceptions.ClientError as e:
        print(e)
    else:
        return response