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
                                            'FromPort': 80,
                                            'ToPort': 80,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            }
                                            ]

                                )
    except botocore.exceptions.ClientError as e:
        print("Create load balancer security group error: " + e)
    else:
        return sg

def create_load_balancer(lb_security_group_id, lb_subnets):

    try:
        lb_client = boto3.client('elbv2')

        lb = lb_client.create_load_balancer(
            Name='application-load-balancer',
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

def create_target_group(vpc_id):

    try:
        lb_client = boto3.client('elbv2')

        tg = lb_client.create_target_group(
            Name='application-target-group',
            Port=80,
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
                    'Port': 80,
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
            Port=80,
            Protocol='HTTP',
        )

    except botocore.exceptions.ClientError as e:
        print(e)
    else:
        return response

#This method is not written yet
def allow_ec2_incoming_traffic_only_from_load_balancer(ec2_instance_security_group_id, ec2_security_group_rule_id, load_balancer_security_group_id):

    ec2_client = boto3.client('ec2')

    try:
        ec2_security_group = ec2_client.describe_security_groups(GroupIds=[ec2_instance_security_group_id])
        print(ec2_instance_security_group_id)
        #To be further written

        
    except botocore.exceptions.ClientErro as e:
        print(e)

def main():

    load_balancer_security_group = create_load_balancer_security_group('vpc-08a8476b32003e8d3') #Temporary testing with my VPC_ID, will use vpc_id we generate
    load_balancer = create_load_balancer(load_balancer_security_group.id, [
        'subnet-073cd7a90757fd3a4', #Temporary using these two subnets, we can update based on our setup
        'subnet-0e7ef3710998198bc',
    ]) 
    target_group = create_target_group('vpc-08a8476b32003e8d3') #Temporary testing with my VPC_ID, will use vpc_id we generate
    registered_target = register_ec2_instance_with_target_group(list(target_group.values())[0][0].get('TargetGroupArn'), 'i-0e53508f76ae0d3f2') #Temporary testing with a hard-coded instance ID, will use instance ID we generate
    listener = create_listener(list(target_group.values())[0][0].get('TargetGroupArn'), list(load_balancer.values())[0][0].get('LoadBalancerArn')) #There is probably a much easier syntax to extra the 'TargetGroupArn' and 'LoadBalancerArn'  
    #allow_ec2_incoming_traffic_only_from_load_balancer('sg-0c39bc5d60f0ed09a', 'sg-08f945743f8d8bdec')

if __name__ == "__main__":
    main()