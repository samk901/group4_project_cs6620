import boto3
import botocore

#See updated create_sg_method below this method which accomodates load balancer security group
#I (Jeff) propose we use second method
def create_sg():
    
    try:
        ec2 = boto3.resource('ec2')
        sg = ec2.create_security_group(GroupName="final_project", Description='SecurityGroupDescription', TagSpecifications=[
                                                                                                        {'ResourceType': 'security-group',
                                                                                                         'Tags': [{'Key': 'SgTagKey', 'Value': 'SgTagVal'}]
                                                                                                        }
                                                                                                          ])
        sg.authorize_ingress(IpPermissions=[{'IpProtocol': 'TCP',
                                            'FromPort': 80,
                                            'ToPort': 80,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            },
                                            {'IpProtocol': 'TCP',
                                            'FromPort': 22,
                                            'ToPort': 22,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            },
                                            {'IpProtocol': 'TCP',
                                            'FromPort': 8000,
                                            'ToPort': 8000,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            },
                                            {'IpProtocol': 'TCP',
                                            'FromPort': 27017,
                                            'ToPort': 27017,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            },
                                            {'IpProtocol': 'TCP',
                                            'FromPort': 3000,
                                            'ToPort': 3000,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            },
                                            {'IpProtocol': 'TCP',
                                            'FromPort': 443,
                                            'ToPort': 443,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            }
                                            ]

                                )

    except botocore.exceptions.ClientError as e:
        print(e)
        pass

    # return sg

#Method to create security group for web servers and application servers.  We can modify if we 
#want different security groups for web vs. application servers.  
#Same as above method, but updated such that HTTP inbound traffic is allowed allowed from load balancer
def create_security_group(sg_name, sg_description, load_balancer_sg_id):
    
    try:
        ec2 = boto3.resource('ec2')
        sg = ec2.create_security_group(GroupName=sg_name, Description=sg_description, TagSpecifications=[
                                                                                                        {'ResourceType': 'security-group',
                                                                                                         'Tags': [{'Key': 'SgTagKey', 'Value': 'SgTagVal'}]
                                                                                                        }
                                                                                                          ])
        sg.authorize_ingress(IpPermissions=[{
                                            'IpProtocol': 'tcp',
                                            'FromPort': 80,
                                            'ToPort': 80,
                                            'UserIdGroupPairs': [{
                                                'GroupId': load_balancer_sg_id
                                            }]
                                            },
                                            {'IpProtocol': 'TCP',
                                            'FromPort': 22,
                                            'ToPort': 22,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            },
                                            {'IpProtocol': 'TCP',
                                            'FromPort': 8000,
                                            'ToPort': 8000,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            },
                                            {'IpProtocol': 'TCP',
                                            'FromPort': 27017,
                                            'ToPort': 27017,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            },
                                            {'IpProtocol': 'TCP',
                                            'FromPort': 3000,
                                            'ToPort': 3000,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            },
                                            {'IpProtocol': 'TCP',
                                            'FromPort': 443,
                                            'ToPort': 443,
                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                            }
                                            ]

                                )

    except botocore.exceptions.ClientError as e:
        print(e)
        pass

# create_security_group('Server security group', 
#                       'Security group for web and application ec2 instances', 
#                       'sg-0abe12d6651793059')
