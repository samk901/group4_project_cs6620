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

#Moving this to create_secuirty_group.py. Initially create the security group associated with
# our EC2 instances to only allow incoming traffic from the load balancer.  Don't want to allow direct http traffic to ec2 instances
def create_secruity_group_with_traffic_only_allowed_from_load_balancer():
    #Method moved to create_security_group.py file
    return True


def main():

    load_balancer_security_group = create_load_balancer_security_group('vpc-08a8476b32003e8d3') #Temporary testing with my VPC_ID, will use vpc_id we generate
    load_balancer = create_load_balancer(load_balancer_security_group.id, [
        'subnet-073cd7a90757fd3a4', #Temporary using these two subnets, we can update based on our setup
        'subnet-0e7ef3710998198bc',
    ]) 
    target_group = create_target_group('vpc-08a8476b32003e8d3') #Temporary testing with my VPC_ID, will use vpc_id we generate
    registered_target1 = register_ec2_instance_with_target_group(list(target_group.values())[0][0].get('TargetGroupArn'), 'i-008b7ba987ee8d6ea') #Temporary testing with a hard-coded instance ID, will use instance ID we generate
    registered_target2 = register_ec2_instance_with_target_group(list(target_group.values())[0][0].get('TargetGroupArn'), 'i-0ce79f06373a78937')
    registered_target3 = register_ec2_instance_with_target_group(list(target_group.values())[0][0].get('TargetGroupArn'), 'i-0e155ee770df0dbe5')
    listener = create_listener(list(target_group.values())[0][0].get('TargetGroupArn'), list(load_balancer.values())[0][0].get('LoadBalancerArn')) #There is probably a much simpler syntax to extract 'TargetGroupArn' and 'LoadBalancerArn'  

if __name__ == "__main__":
    main()