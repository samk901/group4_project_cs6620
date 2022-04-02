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
        print("Create load balander error " + e)
    else:
        return lb


def main():

    load_balancer_security_group = create_load_balancer_security_group('vpc-08a8476b32003e8d3') #Temporary testing with my VPC_ID, will use vpc_id we generate
    load_balancer = create_load_balancer(load_balancer_security_group.id, [
        'subnet-073cd7a90757fd3a4',
        'subnet-0e7ef3710998198bc',
    ]) #Temporary testing with hardcoded subnets

if __name__ == "__main__":
    main()