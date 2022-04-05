import boto3
import botocore

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

#create_sg()
